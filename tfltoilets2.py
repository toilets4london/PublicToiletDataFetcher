# Found more details tfl data at https://content.tfl.gov.uk/lrad-v2.xml

import requests
import xml.etree.ElementTree as ET
import json
import Helpers
import Geocoder
from TransportForLondonToilets import get_borough

# Work in Progress


def build_url(placename):
    encoded = placename.replace(" ","%20")
    return "https://api.tfl.gov.uk/StopPoint/Search?query="+encoded+"&app_key=6da1137fb6314cc7be7a3fb925f42efe"

def latlng(placename):
    url = build_url(placename)
    try:
        jsondata = json.loads(requests.get(url).text)["matches"][0]
        return jsondata["lat"],jsondata["lon"]
    except:
        return "NONE"

def get_data():
    data = requests.get("https://content.tfl.gov.uk/lrad-v2.xml").text
    root = ET.fromstring(data)
    toilets = []
    for station in root.findall("Station"):
        latlngcoords = "NONE"
        name = station.find("StationName").text
        i = 0
        for toilet in station.iter('Toilet'):
            i += 1
        if i > 0:
            latlngcoords = latlng(name)
        if latlngcoords != "NONE":
            full_addr = Geocoder.reverse_geocode(latlngcoords[0], latlngcoords[1])
            borough = get_borough(full_addr)
            FEE = ""
            LOCATION = ""
            INSIDEGATE = False
            ACCESSIBLE = False
            BABYCHANGE = False
            for toilet in station.iter('Toilet'):
                for child in toilet:
                    if child.tag == "FeeCharged":
                        FEE = "Paid" if "y" in child.text.lower() else ""
                    elif child.tag == "Location":
                        if LOCATION == "":
                            LOCATION = child.text
                        elif child.text != LOCATION:
                            LOCATION += child.text + ", "
                    elif child.tag == "InsideGateLine":
                        INSIDEGATE = INSIDEGATE and ("y" in child.text.lower())
                    elif child.tag == "Accessible":
                        ACCESSIBLE = ACCESSIBLE or ("y" in child.text.lower())
                    elif child.tag == "BabyChanging":
                        BABYCHANGE = BABYCHANGE or ("y" in child.text.lower())
            fullname = name
            if INSIDEGATE:
                fullname += " Inside Gate"
            toilets.append({
                "name": fullname,
                "baby_change": BABYCHANGE,
                "wheelchair": ACCESSIBLE,
                "address": name+" "+LOCATION,
                "fee": FEE,
                "latitude": latlngcoords[0],
                "longitude": latlngcoords[1],
                "borough": borough
            })
    with open("Data/processed_data_tfl2.json", "w") as datafile:
        json.dump(toilets,datafile)


