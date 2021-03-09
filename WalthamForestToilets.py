import requests
from bs4 import BeautifulSoup
import Helpers
import json

URL = "https://www.walthamforest.gov.uk/content/public-toilets"


def get_wf_data():
    return requests.get(URL).text


def parse_wf_data(raw_data):
    """ I did not manage to extract the lat / long coords direct from the google maps shortened urls as google would detect suspicious activity and block me
    Therefore instead the lat lng have to be entered manually and I put a link in the json so that i can manually do that """
    soup = BeautifulSoup(raw_data, 'html.parser')
    tables = soup.find_all("table")
    toilets = []
    for t in tables:
        rows = t.find_all("tr")
        for r in rows:
            try:
                t = {}
                name = r.find_all("a")[0]
                name = ' '.join(name.find_all(text=True))
                name = Helpers.only_single_whitespace(name)
                t["name"] = name
                links = r.find_all("a")
                ls = []
                for l in links:
                    ls.append(l["href"])
                t["latitude"] = 0
                t["longitude"] = ls
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
                    if not (Helpers.is_related_to_babychange(text) or Helpers.is_related_to_disabled(text)) :
                        openingtext.append(Helpers.only_single_whitespace(text))
                opening_hours = ", " .join(openingtext)
                t["opening_hours"] = opening_hours
                t["wheelchair"] = disabled
                t["baby_change"] = baby_change
                t["borough"] = "Waltham Forest"
                t["open"] = False
                t["data_source"] = "https://www.walthamforest.gov.uk/content/public-toilets"
                toilets.append(t)
            except:
                pass

    with open("Data/processed_data_waltham_forest.json", "w") as dataFile:
        json.dump(toilets, dataFile)


def extract_waltham_forest_data():
    rawdata = get_wf_data()
    parse_wf_data(rawdata)