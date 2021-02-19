import re
import Helpers
import json

# Stumbled across a cool user generated Google Map at
# https://www.google.com/maps/d/viewer?ie=UTF8&hl=en&msa=0&z=19&mid=1P80hp8j7fNPbO2kFZYNTU3JXwk4&ll=51.46166410960109%2C-0.20279662010626476
# KML file is downloaded from there

NO_DISABLED = "no disabled access"
DISABLED = "disabled access"


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


def is_disabled(placemark):
    if NO_DISABLED in placemark.lower():
        return False
    elif DISABLED in placemark.lower():
        return True
    return False


def is_babychange(placemark):
    return Helpers.is_related_to_babychange(placemark)


def get_info(placemark):
    pattern = re.compile('<description>.*?</description>', re.S)
    info = ""
    try:
        info = re.findall(pattern, placemark)[0]
    finally:
        return info


def is_open(info):
    return not Helpers.is_probably_closed_covid(info)


def get_addr(info):
    elements = Helpers.split_text_with_any_possible_delimiter(info)
    addr = ""
    for e in elements:
        if Helpers.is_probably_an_address(e):
            addr += e
            addr += " "
    return Helpers.cleanxml(Helpers.only_single_whitespace(addr))


def get_hours(info):
    elements = Helpers.split_text_with_any_possible_delimiter(info)
    hours = ""
    for e in elements:
        if Helpers.is_related_to_opening(e):
            hours += e
            hours += " "
    return Helpers.cleanxml(Helpers.only_single_whitespace(hours))


def get_fee(info):
    elements = Helpers.split_text_with_any_possible_delimiter(info)
    fee = ""
    for e in elements:
        if Helpers.is_probably_fee_related(e):
            fee += e
            fee += " "
    return Helpers.cleanxml(Helpers.only_single_whitespace(fee))


def process_wandsworth_data():

    """Source: https://www.google.com/maps/d/viewer?ie=UTF8&hl=en&msa=0&z=19&mid=1P80hp8j7fNPbO2kFZYNTU3JXwk4&ll=51
    .46166410960109%2C-0.20279662010626476 """

    with open("Data/Public & Community Toilets in Wandsworth.kml", "r") as dataFile:
        raw_data = dataFile.read()

    raw_data = raw_data.replace("<![CDATA[", "")
    raw_data = raw_data.replace("]]>", "")
    raw_data = raw_data.replace("@", "")

    toilets = []
    for raw_toilet in find_placemarks(raw_data):
        lat, lng = get_coords(raw_toilet)
        disabled = is_disabled(raw_toilet)
        name = get_name(raw_toilet)
        babychange = is_babychange(raw_toilet)

        info = get_info(raw_toilet)
        addr = get_addr(info)
        opening = get_hours(info)
        isopen = is_open(info)
        fee = get_fee(info)

        if addr == "":
            addr = name + ", Wandsworth"

        toilet = {
            'data_source': 'User generated Google Map called Public & Community Toilets in Wandsworth',
            'borough': 'Wandsworth',
            'address': addr,
            'name': name,
            'latitude': lat,
            'longitude': lng,
            'wheelchair': disabled,
            'open': isopen,
            'baby_change': babychange,
            'opening_hours': opening,
            'fee': fee
        }
        toilets.append(toilet)

    with open("Data/processed_data_wandsworth.json", "w") as jsonFile:
        json.dump(toilets, jsonFile)