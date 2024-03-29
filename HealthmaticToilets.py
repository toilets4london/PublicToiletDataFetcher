import json
import Geocoder
import pandas as pd


def get_name(toilet):
    return toilet['Name']+" "+"Public Toilet"


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
    return toilet['Opening Time']


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
    return df.to_dict(orient='records')


def get_boroughs():
    with open("Data/boroughs.txt", "r") as bfile:
        return bfile.read().split(", ")


def get_latitude(toilet):
    return float(toilet['Latitude'])


def get_longitude(toilet):
    return float(toilet['Longitude'])


def get_address(toilet):
    return toilet['Name']+" "+toilet['Post code']


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
                    full_address = Geocoder.reverse_geocode(get_latitude(t), get_longitude(t))
                    borough = get_borough(boroughs, full_address)
                    toilet = {
                        'data_source': "Dataset sent in by Healthmatic 26/10/20",
                        'address': get_address(t),
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


if __name__ == "__main__":
    healthmatic_excel_to_json()