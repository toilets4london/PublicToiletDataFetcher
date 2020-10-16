
import json
import Geocoder
import pandas as pd


def get_address(toilet):
    street = toilet['Address'].replace('\n', ' ')
    postcode = toilet['Post-code']
    if postcode in street:
        return street
    else:
        return street+" "+postcode

def get_name(toilet):
    area = toilet['Area '].replace('\n', ' ')
    return area+" "+"toilets"

def get_baby_change(toilet):
    try:
        bc = toilet['Baby Changing Available\n\nY/N']
        yes = ['Y', 'y', "Yes", "yes"]
        for ans in yes:
            if ans in bc:
                return True
        return False
    except TypeError:
        return False

def get_disabled(toilet):
    try:
        description = toilet['Type of toilet (WC, Baby Changing, Accessible, Changing Places)']
        yes = ['Disabled', 'disabled', 'wheelchair', "Wheelchair"]
        for ans in yes:
            if ans in description:
                return True
        return False
    except TypeError:
        return False

def get_opening_hours(toilet):
    return toilet['Opening hours (If not 24 hour)'].replace('\n', ' ')


def read_sutton_data():
    df = pd.read_excel('Data/sutton_raw.xlsx')
    print(df.to_dict(orient='records'))
    return df.to_dict(orient='records')


def sutton_excel_to_json():
    data = read_sutton_data()
    with open("Data/processed_data_sutton.json", 'w') as dataFile:
        toilets = []
        for t in data:
            latLng = Geocoder.geocode(get_address(t))
            if latLng != "unavailable":
                toilet = {
                    'data_source': 'Spreadsheet sent in by Sutton council 5/10/2020',
                    'borough':'Sutton',
                    'address': get_address(t),
                    'opening_hours': get_opening_hours(t),
                    'name' : get_name(t),
                    'baby_change' : get_baby_change(t),
                    'latitude' : latLng[0],
                    'longitude' : latLng[1],
                    'wheelchair' : get_disabled(t)
                }
                toilets.append(toilet)
        json.dump(toilets, dataFile)
