import csv
import json
from pyproj import Proj, transform

LOCATION = "LOCATIONTEXT"
E = "GEOX"
N = "GEOY"
FEE = "CHARGEAMOUNT"
OPENINGHOURS = "OPENINGHOURS"

# E/N to lat/lng code from https://webscraping.com/blog/Converting-UK-Easting-Northing-coordinates/

v84 = Proj(proj="latlong", towgs84="0,0,0", ellps="WGS84")
v36 = Proj(proj="latlong", k=0.9996012717, ellps="airy", towgs84="446.448,-125.157,542.060,0.1502,0.2470,0.8421,"
                                                                 "-20.4894")
vgrid = Proj(init="world:bng")


def ENtoLL84(easting, northing):
    """Returns (longitude, latitude) tuple - unintuitive order"""
    vlon36, vlat36 = vgrid(easting, northing, inverse=True)
    return transform(v36, v84, vlon36, vlat36)


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
