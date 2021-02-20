import requests
import json
import Geocoder


URL = "https://api.tfl.gov.uk/StopPoint/Type/NaptanMetroStation?app_key=6da1137fb6314cc7be7a3fb925f42efe"

NAME = "commonName"
LATITUDE = "lat"
LONGITUDE = "lon"

bfile = open("Data/boroughs.txt","r")
BOROUGHS = bfile.read().split(", ")
bfile.close()


def get_borough(location):
    for b in BOROUGHS:
        if b in location:
            return b
    return "Other"


def get_tfl_data():
    with open("Data/transport_for_london_raw.json", "w") as rawDataFile:
        raw_data = requests.get(URL).json()
        json.dump(raw_data, rawDataFile)


def explore_tfl_data():
    with open("Data/transport_for_london_raw.json", "r") as rawDataFile:
        raw_data = json.loads(rawDataFile.read())
    yes = 0
    for point in raw_data:
        if has_toilets(point):
            print(point[NAME]+" has toilets")
            yes += 1
    print(str(yes)+" toilets found")


def has_toilets(stoppoint):
    try:
        properties = stoppoint['additionalProperties']
        for p in properties:
            try:
                if p['key'] == 'Toilets':
                    if 'y' in p['value']:
                        return True
            except KeyError:
                pass
    except KeyError:
        return False


def get_opening_hours(stoppoint):
    opening = ""
    try:
        properties = stoppoint['additionalProperties']
        for p in properties:
            try:
                if p['category'] == 'Opening Time':
                    opening += p['key']
                    opening += " : "
                    opening += p['value']
                    opening += " , "
            except KeyError:
                pass
    finally:
        return opening


def get_tfl_toilets():
    with open("Data/transport_for_london_raw.json", "r") as rawDataFile:
        raw_data = json.loads(rawDataFile.read())
    toilets = []
    for point in raw_data:
        if has_toilets(point):
            full_addr = Geocoder.reverse_geocode(point[LATITUDE], point[LONGITUDE])
            borough = get_borough(full_addr)
            addr = full_addr.replace(", London, Greater London, England", "").replace(", United Kingdom", "")
            t = {
                'name': point[NAME],
                'latitude': point[LATITUDE],
                'longitude': point[LONGITUDE],
                'data_source': 'Transport For London Open Data API',
                'address': addr,
                'opening_hours': get_opening_hours(point),
                'borough': borough
            }
            toilets.append(t)
    with open("Data/processed_data_tfl.json", "w") as dataFile:
        json.dump(toilets, dataFile)

