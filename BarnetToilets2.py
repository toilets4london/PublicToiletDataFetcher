import csv
import json
import Geocoder

# Barnet public toilets data fields
LOCATION = "LocationText"
OPENING_HOURS = "OpeningHours"

def read_barnet_data(path_to_csv="Data/barnet_raw.csv"):
    """  Data downloaded from https://data.gov.uk/dataset/99765417-6e54-4072-a17a-f0d48fe2ce85/public-toilets-2014-15 """
    with open(path_to_csv, newline='\n') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')
        toilets = [row for row in csvreader]
    return toilets

def barnet_libraries_csv_to_json():
    data = read_barnet_data()
    with open("Data/processed_barnet_libraries.json", 'w') as dataFile:
        toilets = []
        for t in data:
            ltlng = Geocoder.geocode(t[LOCATION])
            if ltlng != "unavailable" and "library" in t[LOCATION].lower():
                toilet = {
                    'data_source': 'Data downloaded from https://data.gov.uk/dataset/99765417-6e54-4072-a17a-f0d48fe2ce85/public-toilets-2014-15',
                    'borough':'Barnet',
                    'address': t[LOCATION].replace("opening_hours=",""),
                    'opening_hours': t[OPENING_HOURS].replace("opening_hours=",""),
                    'name' : t[LOCATION].split(",")[0],
                    'latitude' : ltlng[0],
                    'longitude' : ltlng[1],
                    'covid': "Library toilets not open during lockdown",
                    'open': False
                }
                toilets.append(toilet)
            else:
                print(t[LOCATION]+" unavailable")
        json.dump(toilets, dataFile)