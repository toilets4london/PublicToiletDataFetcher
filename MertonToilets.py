import re
import Helpers
import json


def find_placemarks(kml):
    pattern = re.compile('<Placemark>.*?</Placemark>', re.S)
    matches = [x.group() for x in re.finditer(pattern, kml)]
    return matches


def get_name(placemark):
    pattern = re.compile('<name>.*?</name>', re.S)
    name = ""
    try:
        name = Helpers.cleanxml(re.findall(pattern, placemark)[0])
    finally:
        return name


def get_coords(placemark):
    p = Helpers.remove_all_whitespace(placemark)
    pattern = re.compile('<coordinates>.*?</coordinates>', re.S)
    match = Helpers.cleanxml(re.findall(pattern, p)[0])
    all_coors = match.split(",")
    return float(all_coors[1]), float(all_coors[0])


def get_hours(placemark):
    pattern = re.compile('<description>.*?</description>', re.S)
    matches = re.findall(pattern, placemark)
    if len(matches) > 0:
        match = Helpers.cleanxml(matches[0])
        return Helpers.only_single_whitespace(match)
    return ""


def process_merton_data():
    """
    Info on scheme at https://www.merton.gov.uk/streets-parking-transport/community-toilet-scheme
    Map data from https://www.google.com/maps/d/u/0/viewer?mid=1_-vRoCKAAd9IzPprInSprXwZpf8&ll=51.41420980429876%2C-0.17949249999999584&z=15
    """

    with open("Data/merton_community.kml", "r") as dataFile:
        raw_data = dataFile.read()

    raw_data = raw_data.replace("<![CDATA[", "")
    raw_data = raw_data.replace("]]>", "")
    raw_data = raw_data.replace("@", "")

    toilets = []
    for raw_toilet in find_placemarks(raw_data):
        lat, lng = get_coords(raw_toilet)
        name = get_name(raw_toilet)
        opening = get_hours(raw_toilet)
        addr = name + ", Merton"
        toilet = {
            'data_source': 'https://www.merton.gov.uk/streets-parking-transport/community-toilet-scheme',
            'borough': 'Merton',
            'address': addr,
            'name': name,
            'latitude': lat,
            'longitude': lng,
            'opening_hours': opening,
        }
        toilets.append(toilet)

    with open("Data/processed_data_merton.json", "w") as jsonFile:
        json.dump(toilets, jsonFile)
