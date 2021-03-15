import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.royalgreenwich.gov.uk/info/200258/parking_transport_and_streets/810/find_a_public_toilet_in_greenwich"


def get_raw_data():
    return requests.get(URL).text


def process_data(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    table = soup.find_all("tbody")[0]
    rows = table.find_all("tr")
    toilets = []
    for r in rows:
        data = r.find_all("td")
        address = ''.join(data[0].find_all(text=True))
        opening = ''.join(data[1].find_all(text=True))
        fee = (''.join(data[2].find_all(text=True))).replace("None", "")
        additional = ''.join(data[3].find_all(text=True))
        wheelchair = "disabled" in additional.lower()
        baby_change = "baby" in additional.lower() or "change" in additional.lower()
        toilet = {
            'data_source': 'www.royalgreenwich.gov.uk, extracted 15/03/2021',
            'borough': 'Greenwich',
            'address': address,
            'opening_hours': opening,
            'fee': fee,
            'name': 'Public Toilet',
            'baby_change': baby_change,
            'latitude': 0,
            'longitude': 0,
            'wheelchair': wheelchair,
            'open': True
        }
        toilets.append(toilet)
    with open("Data/processed_data_greenwich_nocoords.json", "w") as dataFile:
        # Need to manually add coords to this dataset
        json.dump(toilets, dataFile)


def extract_greenwich_data():
    process_data(get_raw_data())