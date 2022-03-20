import csv
import json
import Geocoder
from datetime import date

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
    today = date.today()
    data = read_barnet_data()
    with open("Data/processed_barnet_libraries.json", 'w') as dataFile:
        toilets = []
        for t in data:
            ltlng = Geocoder.geocode(t[LOCATION])
            if ltlng != "unavailable" and "library" in t[LOCATION].lower():
                toilet = {
                    'data_source': f'https://data.gov.uk/ {today.strftime("%d/%m/%Y")}',
                    'borough': 'Barnet',
                    'address': t[LOCATION].replace("opening_hours=", ""),
                    'opening_hours': t[OPENING_HOURS].replace("opening_hours=", ""),
                    'name': "Library toilets",
                    'latitude': ltlng[0],
                    'longitude': ltlng[1],
                    'open': True
                }
                toilets.append(toilet)
            else:
                pass
        json.dump(toilets, dataFile)


if __name__ == "__main__":
    barnet_libraries_csv_to_json()