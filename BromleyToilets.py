"""
To get the contents of bromley_raw:
- Go to https://bromley.statmap.co.uk/map/Aurora.svc/GetRecordsByPoint?sessionId=7893d79d-ab1c-4a1d-92bd-d59aec55d4ed&x=540500.1488000001&y=166316.67093333337&radius=8000006.69866666666667&scaleDenominator=65536&callback=_jqjsp&_1658618313914=
(replace the sessionId with a newer one)
- Copy the json output to bromley_raw
"""


import json
import re
import Geocoder
from datetime import date


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("â€“", "").replace("\r", "").replace("&#233;", "e").replace("â€™","")
    return cleantext


def get_bromley_toilets():
    print("Bromley toilets [WARNING] Remember to redownload newer raw data!")
    today = date.today()
    with open("Data/bromley_raw.json") as dataFile:
        jsonData = json.loads(dataFile.read())
        htmlData = jsonData['Html']
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
        coords = Geocoder.geocode(toilet["name"]+", "+toilet["address"])
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