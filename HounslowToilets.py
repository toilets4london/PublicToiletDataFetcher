import json
import re
import Geocoder


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def clean_addr(line):
    return line.replace("Rd", "Road").replace("Hounslow", "").replace("&#39;", "").replace("  ", " ")


def get_hounslow_toilets():

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
        print(line)
        if "name" in line.lower():
            t = {"name": line.replace("Name: ", "")}
        if "address" in line.lower():
            a = line.replace("Address: ", "")
            t["address"] = clean_addr(a)
            coords = Geocoder.geocode(a)
            if coords != "unavailable":
                t["data_source"] = "www.hounslow.gov.uk/publictoilets"
                t["latitude"] = coords[0]
                t["longitude"] = coords[1]
                t["borough"] = "Hounslow"
                toilets.append(t)
            else:
                print("UNAVAILABLE "+t["name"])
            t = {}
    with open("Data/processed_data_hounslow.json", "w") as dataFile:
        json.dump(toilets, dataFile)

