import json
import re
import Geocoder
from datetime import date
import requests
from urllib.parse import quote


def get_data():
    script = quote(")A/GYZot3rBkZJ7xL8zSgDFDBiRkrqriP3K+bJsgj/g2i9W7WZN4ffG9FUVstNhS9PDYlFZiVIN03bQh0o+wk6Q==")
    resp = requests.get(
        f"https://bromley.statmap.co.uk/map/Aurora.svc/RequestSession?userName=)s%2Ffolr69XyiGXRQuL%2FeXrw%3D%3D&password=&script={script}", headers={
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        })
    j = resp.text
    sid = re.findall('"SessionId":"([A-Za-z0-9_-]*)"', j)[0]
    requests.get(f"https://bromley.statmap.co.uk/map/Aurora.svc/OpenScriptMap?sessionId={sid}")
    resp = requests.get(
        f"https://bromley.statmap.co.uk/map/Aurora.svc/GetRecordsByPoint?sessionId={sid}&x=540500.1488000001&y=166316.67093333337&radius=860000000000.69866666666667&scaleDenominator=65536&script={script}",
        headers={
            "Accept": "*/*",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Referrer": "https://bromley.statmap.co.uk/map/Aurora.svc/run?script=)A/GYZot3rBkZJ7xL8zSgDFDBiRkrqriP3K+bJsgj/g2i9W7WZN4ffG9FUVstNhS9PDYlFZiVIN03bQh0o+wk6Q==&nocache=037c4c4a-ace9-df3d-c2d6-81463a4bfe70&resize=always"
        })
    return resp.json()["Html"]


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("â€“", "").replace("\r", "").replace("&#233;", "e").replace("â€™", "")
    return cleantext


def get_bromley_toilets():
    today = date.today()
    htmlData = get_data()
    lines = htmlData.split("\n")
    toilets = [[cleanhtml(p) for p in l.split("<br/>")] for l in lines]
    data = []
    for t in toilets:
        toilet = {}
        if len(t) < 3:
            continue
        toilet["name"] = t[0]
        toilet["address"] = t[1]
        toilet["wheelchair"] = 'Disabled: Y' in t
        toilet["baby_change"] = 'Baby Changing: Y' in t
        for p in t:
            if "Times" in p:
                toilet["opening_hours"] = p.replace("Times: ", "")
        coords = Geocoder.geocode(toilet["name"] + ", " + toilet["address"])
        if coords == "unavailable":
            print("Can only geocode postcode")
            parts = toilet["address"].split(" ")
            post = " ".join([parts[-2], parts[-1]])
            post = post.replace(",", "").strip()
            coords = Geocoder.geocode(post)
        if coords != "unavailable":
            toilet["latitude"] = coords[0]
            toilet["longitude"] = coords[1]
            toilet["data_source"] = f'bromley.gov.uk/street-care-cleaning/community-public-toilets {today.strftime("%d/%m/%Y")}'
            toilet["borough"] = "Bromley"
            data.append(toilet)
        else:
            print("Failed geocoding", toilet["address"])
    with open("Data/processed_data_bromley.json", "w") as dataFile:
        json.dump(data, dataFile)


if __name__ == "__main__":
    get_bromley_toilets()