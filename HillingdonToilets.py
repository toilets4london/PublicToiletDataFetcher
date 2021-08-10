import csv
import json
from Helpers import ENtoLL84

LOCATION = "LOCATIONTEXT"
E = "GEOX"
N = "GEOY"
FEE = "CHARGEAMOUNT"
OPENINGHOURS = "OPENINGHOURS"


def read_hillingdon_data(path_to_csv="Data/hillingdon_export_public_conveniences.csv"):
    with open(path_to_csv, newline='\n') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')
        toilets = [row for row in csvreader]
    return toilets


def addr_builder(toilet):
    return toilet[LOCATION].replace("Public Convenience ", "")


def get_fee(toilet):
    fee_string = toilet[FEE]
    if int(float(fee_string)) == 0:
        return "Free"
    else:
        return fee_string


def hillingdon_csv_to_json():
    data = read_hillingdon_data()
    with open("Data/processed_data_hillingdon.json", 'w') as dataFile:
        toilets = []
        for t in data:
            lng, lat = ENtoLL84(t[E], t[N])
            toilet = {
                'data_source': 'Dataset sent in by London Borough of Hillingdon on 08/01/21',
                'borough': 'Hillingdon',
                'address': addr_builder(t),
                'opening_hours': t[OPENINGHOURS],
                'name': "Public Convenience",
                'latitude': lat,
                'longitude': lng,
                'fee': get_fee(t),
                'open': True
            }
            toilets.append(toilet)
        json.dump(toilets, dataFile)


hillingdon_csv_to_json()
