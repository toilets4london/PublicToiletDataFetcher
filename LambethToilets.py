import json
import Geocoder
import pandas as pd
import re


def get_address(toilet):
    return toilet['Full Address']

def get_name(toilet):
    return toilet['Site Name']

def get_disabled(toilet):
    desc = toilet['Toilets on site'].lower()
    matches = ["disabled", "wheelchair"]
    for m in matches:
        if m in desc:
            return True
    return False

def get_baby_change(toilet):
    desc = toilet['Baby change Facilities'].lower()
    if "no" in desc:
        return False
    return True

def read_lambeth_data():
    df = pd.read_excel('Data/lambeth_raw.xls', header=2)
    return df.to_dict(orient='records')

def get_postcode(toilet):
    pattern = re.compile('(([A-Z][0-9]{1,2})|(([A-Z][A-HJ-Y][0-9]{1,2})|(([A-Z][0-9][A-Z])|([A-Z][A-HJ-Y][0-9]?[A-Z])))) [0-9][A-Z]{2}')
    m = pattern.search(toilet['Full Address'])
    if m:
        return m.group()
    else:
        return ""

def get_latLng(toilet):
    longest_addr = toilet['Site Name']+" "+toilet['Full Address']
    medium_addr = toilet['Site Name']+" "+get_postcode(toilet)
    short_addr = toilet['Full Address']
    shortest_addr = get_postcode(toilet)
    for a in [longest_addr, medium_addr, short_addr, shortest_addr]:
        latLng = Geocoder.geocode(a)
        if latLng != "unavailable":
            return latLng
    return latLng


def lambeth_excel_to_json():
    data = read_lambeth_data()
    with open("Data/processed_data_lambeth.json", 'w') as dataFile:
        toilets = []
        for t in data:
            latLng = get_latLng(t)
            if latLng != "unavailable":
                toilet = {
                    'data_source' : 'Lambeth Council sent in spreadsheet 22/10/2020',
                    'borough':'Lambeth',
                    'address': get_address(t),
                    'opening_hours': "",
                    'name' : get_name(t),
                    'baby_change' : get_baby_change(t),
                    'latitude' : latLng[0],
                    'longitude' : latLng[1],
                    'wheelchair' : get_disabled(t)
                }
                toilets.append(toilet)
            else:
                print("Error geocoding %s"%get_address(t))
        json.dump(toilets, dataFile)
