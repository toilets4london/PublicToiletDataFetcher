import requests
from bs4 import BeautifulSoup
import json
import Helpers

URL = "https://www.bexley.gov.uk/services/parking-transport-and-streets/public-toilets/reporting-issues-public-toilets"


def get_raw_data():
    return requests.get(URL).text


def process_data(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    table = soup.find_all("tbody")[0]
    rows = table.find_all("tr")
    toilets = []
    for r in rows:
        header = r.find_all("th")
        name = ''.join(header[0].find_all(text=True))
        data = r.find_all("td")
        address_col = data[0]
        info_col = data[1]
        address_parts = [Helpers.only_single_whitespace(part) for part in address_col.find_all(text=True)]
        address_parts = [part for part in address_parts if part != "" and part.lower() != "map"]
        info_parts = [Helpers.only_single_whitespace(part) for part in info_col.find_all(text=True)]
        info_parts = [part for part in info_parts if part != ""]
        info = "".join(info_parts)
        opening = " ".join([a for a in info_parts if not Helpers.is_related_to_babychange(a) and not Helpers.is_related_to_disabled(a)])
        wheelchair = "disabled" in info.lower()
        baby_change = "baby" in info.lower()
        radar = "radar" in info.lower()
        toilet = {
            'data_source': 'www.bexley.gov.uk, extracted 15/03/2021',
            'borough': 'Bexley',
            'address': " ".join(address_parts),
            'opening_hours': opening,
            'name': name,
            'baby_change': baby_change,
            'latitude': 0,
            'longitude': 0,
            'wheelchair': wheelchair,
            'open': True
        }
        toilets.append(toilet)
    with open("Data/processed_data_bexley_nocoords.json", "w") as dataFile:
        # Need to manually add coords to this dataset
        json.dump(toilets, dataFile)


def extract_bexley_data():
    process_data(get_raw_data())

extract_bexley_data()