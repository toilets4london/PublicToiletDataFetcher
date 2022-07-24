"""
To get the contents of hounslow_raw:
- Go to https://maps.hounslow.gov.uk/map/Aurora.svc/GetRecordsByPoint?sessionId=dfd98443-8798-4176-94c8-9aa4b10c541b&x=510638.7263847503&y=178875.600798287&radius=860000.69866666666667&scaleDenominator=65536&callback=_jqjsp&_1658616689635=
(replace the sessionId with a newer one)
- Copy the json output to hounslow_raw
"""


import json
import re
import Geocoder
from datetime import date


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def clean_addr(line):
    return line.replace("Rd", "Road").replace("Hounslow", "").replace("&#39;", "").replace("  ", " ")


def get_hounslow_toilets():
    print("Hounslow toilets [WARNING] Remember to redownload newer raw data!")
    today = date.today()

    """ https://maps.hounslow.gov.uk/map/Aurora.svc/run?script=%5cAurora%5cFind_your_nearest_Public+Toilets
    .AuroraScript%24&nocache=747441043&resize=always """

    with open("Data/hounslow_raw.json") as dataFile:
        jsonData = json.loads(dataFile.read())
        htmlData = jsonData['Html']
        lines = htmlData.split("\n")
        lines = [cleanhtml(l).replace("\r", "") for l in lines]
    toilets = []
    t = {}
    for line in lines:
        if "name" in line.lower():
            t = {"name": line.replace("Name: ", "")}
        if "address" in line.lower():
            a = line.replace("Address: ", "")
            t["address"] = clean_addr(a)
            coords = Geocoder.geocode(t["name"]+", "+a)
            if coords == "unavailable":
                print("Can only geocode postcode")
                parts = a.split(" ")
                coords = Geocoder.geocode(" ".join([parts[-2], parts[-1]]))
            if coords != "unavailable":
                t["data_source"] = f'hounslow.gov.uk/publictoilets {today.strftime("%d/%m/%Y")}'
                t["latitude"] = coords[0]
                t["longitude"] = coords[1]
                t["borough"] = "Hounslow"
                toilets.append(t)
            else:
                print("UNAVAILABLE ", a)
            t = {}
    with open("Data/processed_data_hounslow.json", "w") as dataFile:
        json.dump(toilets, dataFile)


if __name__ == "__main__":
    get_hounslow_toilets()