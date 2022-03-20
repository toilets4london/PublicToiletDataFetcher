import json
import requests
import Geocoder
import pandas as pd
from datetime import date


def get_address(toilet):
    name = toilet['Unnamed: 0'].replace("toilet","").replace("Toilet","")
    street = toilet['Billing Address Line 1']
    borough = "Lewisham, London"
    postcode = toilet['Billing Zip/Postal Code']
    if street != "" and postcode != "":
        return street + ", " + borough + ", "+postcode
    else:
        str = ""
        for s in [name, street, borough, postcode]:
            if s != "":
                str += s
                str += " "
        return str


def get_name(toilet):
    return toilet['Unnamed: 0']


def get_baby_change(toilet):
    baby_change = str(toilet['Baby Change?'])
    yes_answers = ['1', 'yes', 'Yes', 'y', 'Y']
    for y in yes_answers:
        if y in baby_change:
            return True
    return False


def get_disabled(toilet):
    disabled = str(toilet['Disabled Access?'])
    yes_answers = ['1', 'yes', 'Yes', 'y', 'Y']
    for y in yes_answers:
        if y in disabled:
            return True
    return False


def get_opening_hours(toilet):
    return toilet['Opening Hours']


def read_lewisham_data():
    df = pd.read_excel('Data/lewisham_raw.xlsx').fillna("")
    return df.to_dict(orient='records')


def lewisham_excel_to_json():
    '''Leads to a few geocoding errors as many addresses are not full - see web scraping solution below'''
    data = read_lewisham_data()
    print(data)
    with open("Data/processed_data_lewisham.json", 'w') as dataFile:
        toilets = []
        for t in data:
            name = get_name(t)
            address = get_address(t)
            disabled = get_disabled(t)
            babychange = get_baby_change(t)
            opening = get_opening_hours(t)
            print(address)
            latLng = Geocoder.geocode(address)
            if latLng != "unavailable":
                toilet = {
                    'data_source':"Lewisham Community Toilets dataset (updated for Covid)",
                    'borough':"Lewisham",
                    'address': address,
                    'opening_hours': opening,
                    'name' : name,
                    'baby_change' : babychange,
                    'latitude' : latLng[0],
                    'longitude' : latLng[1],
                    'wheelchair' : disabled
                }
                toilets.append(toilet)
            else:
                print("THERE WAS AN ERROR GEOCODING THIS TOILET'S ADDRESS")
        json.dump(toilets, dataFile)


def is_disabled(toilet, official_data_i_was_sent):
    for t in official_data_i_was_sent:
        # Trying to match toilet from api url to toilet in spreadsheet
        if t['Billing Zip/Postal Code'].replace(" ","") == toilet['zip'].replace(" ",""):
            return get_disabled(t)
        if t['Unnamed: 0'].replace(" ","") == toilet['title']['raw'].replace(" ",""):
            return get_disabled(t)
    return False


def is_baby_change(toilet, official_data_i_was_sent):
    for t in official_data_i_was_sent:
        if t['Billing Zip/Postal Code'].replace(" ","") == toilet['zip'].replace(" ",""):
            return get_baby_change(t)
        if t['Unnamed: 0'].replace(" ","") == toilet['title']['raw'].replace(" ",""):
            return get_baby_change(t)
    return False


def get_covid_info(toilet, official_data_i_was_sent):
    for t in official_data_i_was_sent:
        if t['Billing Zip/Postal Code'].replace(" ","") == toilet['zip'].replace(" ",""):
            return t['What additional precautions/equipment are you putting in place in order to ensure public safety? (eg. signage, extra cleaning, hand sanitising station)']
        if t['Unnamed: 0'].replace(" ","") == toilet['title']['raw'].replace(" ",""):
            return t['What additional precautions/equipment are you putting in place in order to ensure public safety? (eg. signage, extra cleaning, hand sanitising station)']
    return ""



def is_in_official_data(toilet, official_data_i_was_sent):
    for t in official_data_i_was_sent:
        if t['Billing Zip/Postal Code'].replace(" ", "").lower() == toilet['zip'].replace(" ", "").lower():
            return True
        if t['Unnamed: 0'].replace(" ", "") == toilet['title']['raw'].replace(" ", ""):
            return True
    return False


def lewisham_json_api_to_filtered_json():

    """ Easier way to get accurate lat long coordinates because
    excel file sent to me did not have full addresses for all toilets """

    official_data_i_was_sent = read_lewisham_data()
    today = date.today()
    # Found by examining source of https://www.lewishamlocal.com/community-toilets-map/
    # Place category 8 corresponds to public toilets
    API_URL = "https://www.lewishamlocal.com/wp-json/geodir/v2/places?gd_placecategory=8&per_page=100"
    response = requests.get(API_URL)
    with open("Data/lewisham_raw.json", 'w') as dataFile:
        json.dump(obj = response.json(), fp = dataFile)
    with open("Data/lewisham_raw.json") as datafile:
        toilets = []
        d = json.loads(datafile.read())
        for t in d:
            name = t['title']['raw']
            address = t['street']+" "+t['zip']
            latitude = t['latitude']
            longitude = t['longitude']
            opening = t['timing']
            disabled = is_disabled(t, official_data_i_was_sent)
            babychange = is_disabled(t, official_data_i_was_sent)
            filtered_dict = {}
            filtered_dict['data_source'] = f'lewishamlocal.com/projects/communitytoilets/ {today.strftime("%d/%m/%Y")}'
            filtered_dict['address'] = address
            filtered_dict['latitude'] = latitude
            filtered_dict['longitude'] = longitude
            filtered_dict['borough'] = "Lewisham"
            filtered_dict['wheelchair'] = disabled
            filtered_dict['name'] = name
            filtered_dict['opening_hours'] = opening
            filtered_dict['baby_change'] = babychange
            filtered_dict['open'] = is_in_official_data(t, official_data_i_was_sent)
            filtered_dict['covid'] = get_covid_info(t, official_data_i_was_sent)
            toilets.append(filtered_dict)
    with open("Data/processed_data_lewisham_2.json", 'w') as dataFile:
        json.dump(toilets, dataFile)


if __name__ == "__main__":
    lewisham_json_api_to_filtered_json()