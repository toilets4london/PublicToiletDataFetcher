import re
import Helpers
import json

# Stumbled across a cool user generated Google Map at
# https://www.google.com/maps/d/viewer?ie=UTF8&hl=en&msa=0&z=19&mid=1P80hp8j7fNPbO2kFZYNTU3JXwk4&ll=51.46166410960109%2C-0.20279662010626476
# KML file is downloaded from there

NO_DISABLED = "no disabled access"
DISABLED = "disabled access"


def is_disabled(info):
    if NO_DISABLED in info.lower():
        return False
    elif DISABLED in info.lower():
        return True
    return False


def is_babychange(info):
    if "baby" in info.lower():
        return True
    return False


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


def get_info(placemark):
    pattern = re.compile('<description>.*?</description>', re.S)
    info = ""
    try:
        info = Helpers.cleanxml(re.findall(pattern, placemark)[0])
    finally:
        return info


def get_addr(info):
    addr = ""
    try:
        addr = info.split(".")[0]
        if "disabled" in addr or "baby" in addr:
            addr = ""
    finally:
        return addr


def get_open(info):
    """ keywords that indicate that toilet is probably closed during lockdown """
    keywords = ["library", "caf", "centre", "bar", "brasserie", "public house", "pub", "room", "house", "the", "club", "centre", "restaurant", "court"]
    for k in keywords:
        if k in info.lower():
            return False
    return True


def process_wandsworth_data():

    """Source: https://www.google.com/maps/d/viewer?ie=UTF8&hl=en&msa=0&z=19&mid=1P80hp8j7fNPbO2kFZYNTU3JXwk4&ll=51
    .46166410960109%2C-0.20279662010626476 """

    with open("Data/Public & Community Toilets in Wandsworth.kml", "r") as dataFile:
        raw_data = dataFile.read()

    raw_data = raw_data.replace("<![CDATA[@ ", "")
    raw_data = raw_data.replace("]]>", "")
    raw_data = raw_data.replace("@", "")

    toilets = []
    for p in find_placemarks(raw_data):
        raw_toilet = Helpers.only_single_whitespace(p)
        lat, lng = get_coords(raw_toilet)
        info = get_info(raw_toilet)
        disabled = is_disabled(info)
        addr = get_addr(info)
        name = get_name(p)
        if addr == "":
            addr = name + ", Wandsworth"
        isopen = get_open(info)
        babychange = is_babychange(info)
        toilet = {
            'data_source': 'User generated Google Map called "Public & Community Toilets in Wandsworth"',
            'borough': 'Wandsworth',
            'address': addr,
            'name': name,
            'latitude': lat,
            'longitude': lng,
            'wheelchair': disabled,
            'open': isopen,
            'baby_change': babychange
        }
        toilets.append(toilet)

    with open("Data/processed_data_wandsworth.json", "w") as jsonFile:
        json.dump(toilets, jsonFile)