import requests
from bs4 import BeautifulSoup
import Helpers
import json
from datetime import date

URL = "https://www.walthamforest.gov.uk/neighbourhoods/public-toilets"


def get_wf_data():
    return requests.get(URL).text


def lat_lng_from_google_maps_url(url):
    r = requests.get(url, allow_redirects=False)
    red = r.headers['Location'].split("!")
    lat = float(red[-2][2:10])
    lng = float(red[-1][2:10])
    return lat, lng


def parse_wf_data(raw_data):
    soup = BeautifulSoup(raw_data, 'html.parser')
    tables = soup.find_all("table")
    toilets = []
    today = date.today()
    for t in tables:
        rows = t.find_all("tr")
        for r in rows:
            try:
                t = {}
                name = r.find_all("a")[0]
                lat, lng = lat_lng_from_google_maps_url(name["href"])
                name = ' '.join(name.find_all(text=True))
                name = Helpers.only_single_whitespace(name)
                t["name"] = name
                t["latitude"] = lat
                t["longitude"] = lng
                addr = r.find_all("p")[0]
                addr = ' '.join(addr.find_all(text=True))
                addr = Helpers.only_single_whitespace(addr)
                addr = Helpers.only_single_whitespace(addr)
                t["address"] = addr
                disabled = False
                baby_change = False
                opening = r.find_all("p")
                opening = opening[1:len(opening)]
                openingtext = []
                for o in opening:
                    text = ' '.join(o.find_all(text=True))
                    if Helpers.is_related_to_disabled(text):
                        disabled = True
                    if Helpers.is_related_to_babychange(text):
                        baby_change = True
                    if not (Helpers.is_related_to_babychange(text) or Helpers.is_related_to_disabled(text)):
                        openingtext.append(Helpers.only_single_whitespace(text))
                opening_hours = ", ".join(openingtext)
                t["opening_hours"] = opening_hours
                t["wheelchair"] = disabled
                t["baby_change"] = baby_change
                t["borough"] = "Waltham Forest"
                t["open"] = True
                t["data_source"] = f'walthamforest.gov.uk/neighbourhoods/public-toilets {today.strftime("%d/%m/%Y")}'
                toilets.append(t)
            except:
                pass

    with open("Data/processed_data_waltham_forest.json", "w") as dataFile:
        json.dump(toilets, dataFile)


def extract_waltham_forest_data():
    rawdata = get_wf_data()
    parse_wf_data(rawdata)


if __name__ == "__main__":
    extract_waltham_forest_data()
