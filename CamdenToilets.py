import csv
import json

# Camden public toilets data fields
NAME = 'Name'
OPENING_HOURS = 'Opening Hours'
BUILDING_NAME = 'Building Name'
BUILDING_NUMBER = 'Building Number'
STREET = 'Street'
POSTCODE = 'Postcode'
EASTING = 'Easting'
NORTHING = 'Northing'
LONGITUDE = 'Longitude'
LATITUDE = 'Latitude'
LAST_UPLOADED = 'Last Uploaded'


def read_camden_data(path_to_csv="Data/Public_toilets.csv"):
    """  Data downloaded from https://opendata.camden.gov.uk/People-Places/Public-toilets/v8f3-kxqp """
    with open(path_to_csv, newline='\n') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')
        toilets = [row for row in csvreader]
    return toilets


def addr_builder(toilet):
    return "%s %s, %s" % (toilet[BUILDING_NUMBER],toilet[STREET],toilet[POSTCODE])


def camden_csv_to_json():
    camden_data = read_camden_data()
    with open("Data/camden_data.json", 'w') as dataFile:
        toilets = []
        for t in camden_data:
            toilet = {
                'borough':'Camden',
                'address': addr_builder(t),
                'opening_hours': t[OPENING_HOURS],
                'name' : t[NAME],
                'latitude' : t[LATITUDE],
                'longitude' : t[LONGITUDE]
            }
            toilets.append(toilet)
        json.dump(toilets, dataFile)