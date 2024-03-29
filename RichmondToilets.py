import requests
import json
import re
from datetime import date

RICHMOND_TOILET_DATA_URL = 'http://www2.richmond.gov.uk/lbrservicesSP/offers/SpendAPenny/'


## This script is currently not functional as the map is no longer displaying any community toilets (!)

def get_name(toilet):
    if toilet['type'] == "Community Toilet Scheme":
        return toilet['name'] + " Community Toilet Scheme"
    else:
        return toilet['name']


def get_address(toilet):
    return toilet["address1"] + " " + toilet["postcode"]


def get_latitude(toilet):
    return float(toilet["lat"])


def get_longitude(toilet):
    return float(toilet["long"])


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_opening_hours(toilet):
    hours = cleanhtml(toilet["hours"])
    days = cleanhtml(toilet["days"])
    opening = hours + " " + days
    if opening == "Hours:  Days open: ":
        return ""
    else:
        return hours + " " + days


def get_baby_change(toilet):
    facilities = cleanhtml(toilet["toilets"])
    list_of_words = ["Baby", "baby", "change", "Change", "Changing", "changing"]
    for w in list_of_words:
        if w in facilities:
            return True
    return False


def get_disabled(toilet):
    facilities = cleanhtml(toilet["toilets"])
    list_of_words = ["disabled", "Disabled", "wheelchair", "Wheelchair"]
    for w in list_of_words:
        if w in facilities:
            return True
    return False


def get_richmond_data():
    response = requests.get(RICHMOND_TOILET_DATA_URL)
    with open("Data/RichmondToiletsRaw.json", 'w') as dataFile:
        # strange character
        dataFile.write(response.text.replace('\u0009', ''))


def read_raw_data():
    with open("Data/RichmondToiletsRaw.json") as datafile:
        d = json.loads(datafile.read())
    return d


def clean_data():
    today = date.today()
    richmond_data = read_raw_data()
    toilets = richmond_data['businesses']
    wcs = []
    for t in toilets:
        filtered_dict = {}
        if t['CTA'] == "1" and t["lat"] != "" and t["long"] != "":
            filtered_dict['data_source'] = f'richmond.gov.uk/community_toilet_scheme {today.strftime("%d/%m/%Y")}'
            filtered_dict['address'] = get_address(t)
            filtered_dict['latitude'] = get_latitude(t)
            filtered_dict['longitude'] = get_longitude(t)
            filtered_dict['borough'] = "Richmond upon Thames"
            filtered_dict['wheelchair'] = get_disabled(t)
            filtered_dict['name'] = get_name(t)
            filtered_dict['opening_hours'] = get_opening_hours(t)
            filtered_dict['baby_change'] = get_baby_change(t)
            wcs.append(filtered_dict)
    return wcs


def write_cleaned_data_richmond(newpath="Data/processed_data_richmond.json"):
    data = clean_data()
    with open(newpath, 'w') as dataFile:
        json.dump(data, dataFile)


def get_data():
    get_richmond_data()
    write_cleaned_data_richmond()


if __name__ == "__main__":
    get_data()
