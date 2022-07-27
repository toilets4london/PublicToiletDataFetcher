import json
import re
import Geocoder
from datetime import date
import requests


def get_data():
    resp = requests.get(
        "https://maps.hounslow.gov.uk/map/Aurora.svc/RequestSession?userName=GUEST&password=&script=%5CAurora%5CFind_your_nearest_Public+Toilets.AuroraScript%24")
    sid = re.findall('"SessionId":"([A-Za-z0-9_-]*)"', resp.text)[0]
    requests.get(f"https://maps.hounslow.gov.uk/map/Aurora.svc/OpenScriptMap?sessionId={sid}")
    resp = requests.get(
        f"https://maps.hounslow.gov.uk/map/Aurora.svc/GetRecordsByPoint?sessionId={sid}&x=515918.6751847503&y=174584.016798287&radius=860000000000.69866666666667&scaleDenominator=65536")
    return resp.json()["Html"]


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def clean_addr(line):
    return line.replace("Rd", "Road").replace("Hounslow", "").replace("&#39;", "").replace("  ", " ")


def get_hounslow_toilets():
    today = date.today()
    htmlData = get_data()
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
            coords = Geocoder.geocode(t["name"] + ", " + a)
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
