import requests
import json
import Geocoder
from datetime import date


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
        monfrifrom = ""
        monfrito = ""
        satfrom = ""
        satto = ""
        sunfrom = ""
        sunto = ""
        for p in properties:
            try:
                if p['category'] == 'Opening Time':
                    key = p["key"]
                    key = key.strip()
                    value = p["value"]
                    if key == "MonFriTo":
                        monfrito = value
                    elif key == "MonFriFrom":
                        monfrifrom = value
                    elif key == "SatTo":
                        satto = value
                    elif key == "SatFrom":
                        satfrom = value
                    elif key == "SunTo":
                        sunto = value
                    elif key == "SunFrom":
                        sunfrom = value
            except KeyError:
                pass
        if monfrifrom != "":
            opening = f"Mon-Fri {monfrifrom}-{monfrito}"
        if satfrom != "":
            opening += f", Sat {satfrom}-{satto}"
        if sunfrom != "":
            opening += f", Sun {sunfrom}-{sunto}"
    finally:
        return opening


def get_tfl_toilets():
    with open("Data/transport_for_london_raw.json", "r") as rawDataFile:
        raw_data = json.loads(rawDataFile.read())
    toilets = []
    today = date.today()
    for point in raw_data:
        if has_toilets(point):
            full_addr = Geocoder.reverse_geocode(point[LATITUDE], point[LONGITUDE])
            borough = get_borough(full_addr)
            if borough != "Other":
                addr = full_addr.replace(", London, Greater London, England", "").replace(", United Kingdom", "")
                addr = addr.split(",")
                addr = ",".join([addr[0], addr[1], addr[-1]])
                t = {
                    'name': point[NAME],
                    'latitude': point[LATITUDE],
                    'longitude': point[LONGITUDE],
                    'data_source': f'TFL Open Data API {today.strftime("%d/%m/%Y")}',
                    'address': addr,
                    'opening_hours': get_opening_hours(point),
                    'borough': borough
                }
                toilets.append(t)
    with open("Data/processed_data_tfl.json", "w") as dataFile:
        json.dump(toilets, dataFile)


if __name__ == "__main__":
    get_tfl_toilets()