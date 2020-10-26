import json
import Geocoder
import pandas as pd


def get_name(toilet):
    if toilet['charges']=="20p":
        return toilet['Name']+" "+"Automatic Public Toilet"
    return toilet['Name']


def get_baby_change(toilet):
    baby_change = toilet['Baby changing'].lower()
    if 'y' in baby_change:
        return True
    return False


def get_disabled(toilet):
    disabled = toilet['Disabled Accessibility'].lower()
    if 'y' in disabled:
        return True
    return False


def get_opening_hours(toilet):
    return toilet['Disabled Accessibility']


def get_charge(toilet):
    return toilet['charges']


def get_borough(bouroughs, address):
    for b in bouroughs:
        if b in address:
            return b
    return ""


# I had to manually look up the lat / long co-oordinates of these toilets as the addresses were very incomplete
def read_healthmatic_data():
    df = pd.read_excel('Data/healthmatic_raw.xlsx', header=3, usecols="B:Q").fillna("")
    print(df.to_dict(orient='records'))
    return df.to_dict(orient='records')


def get_boroughs():
    with open("Data/boroughs.txt", "r") as bfile:
        return bfile.read().split(", ")


def get_latitude(toilet):
    return float(toilet['Latitude'])


def get_longitude(toilet):
    return float(toilet['Longitude'])


def healthmatic_excel_to_json():
    """Leads to geocoding errors as many addresses are not full"""
    data = read_healthmatic_data()
    boroughs = get_boroughs()
    with open("Data/processed_data_healthmatic.json", 'w') as dataFile:
        toilets = []
        for t in data:
            # Royal parks data was collected seperately
            if t['Group'] != 'Royal Parks':
                try:
                    full_address = Geocoder.reverse_geocode(get_latitude(t), get_longitude(t)).replace('London, Greater London, England,', '')
                    full_address = full_address.replace(', United Kingdom', '')
                    print("Full address: " + full_address)
                    borough = get_borough(boroughs, full_address)
                    toilet = {
                        'data_source': "Dataset sent in by Healthmatic 26/10/20",
                        'address': full_address,
                        'opening_hours': get_opening_hours(t),
                        'name':  get_name(t),
                        'baby_change': get_baby_change(t),
                        'latitude': get_latitude(t),
                        'longitude': get_longitude(t),
                        'wheelchair': get_disabled(t),
                        'fee': get_charge(t),
                        'borough': borough
                    }
                    toilets.append(toilet)
                except:
                    print('Error reverse geocoding %s'%get_name(t))
        json.dump(toilets, dataFile)

healthmatic_excel_to_json()