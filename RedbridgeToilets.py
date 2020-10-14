import json
import Geocoder
import pandas as pd


def get_address(toilet):
    street = toilet['Name']
    postcode = toilet['Postcode']
    return street+" "+postcode

def get_name(toilet):
    return toilet['Name']

def get_disabled(toilet):
    disabled = toilet['Disabled']
    if disabled == 'Y' or disabled == 'y':
        return True
    return False

def get_opening_hours(toilet):
    return toilet['Opening hours']


def read_redbridge_data():
    df = pd.read_excel('Data/redbridge_raw.xlsx')
    print(df.to_dict(orient='records'))
    return df.to_dict(orient='records')


def redbridge_excel_to_json():
    data = read_redbridge_data()
    with open("Data/processed_data_redbridge.json", 'w') as dataFile:
        toilets = []
        for t in data:
            latLng = Geocoder.geocode(get_address(t))
            if latLng != "unavailable":
                toilet = {
                    'borough':'Redbridge',
                    'address': get_address(t),
                    'opening_hours': get_opening_hours(t),
                    'name' : get_name(t),
                    'baby_change' : False,
                    'latitude' : latLng[0],
                    'longitude' : latLng[1],
                    'wheelchair' : get_disabled(t)
                }
                toilets.append(toilet)
        json.dump(toilets, dataFile)
