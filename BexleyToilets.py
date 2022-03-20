import requests
from bs4 import BeautifulSoup
import json
import Helpers
from datetime import date

URL = "https://www.bexley.gov.uk/services/parking-transport-and-streets/public-toilets/reporting-issues-public-toilets"


def get_raw_data():
    return requests.get(URL).text


def process_data(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    table = soup.find_all("tbody")[0]
    rows = table.find_all("tr")
    toilets = []
    today = date.today()
    for r in rows:
        header = r.find_all("th")
        name = ''.join(header[0].find_all(text=True))
        data = r.find_all("td")
        link = r.find_all(href=True)
        lat, lng = 0, 0
        if len(link) > 0:
            link = link[0]["href"]
            r = requests.get(link, allow_redirects=False)
            red = r.headers['Location'].split("!")
            lat = float(red[-2][2:10])
            lng = float(red[-1][2:10])
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
        address = " ".join(address_parts)
        if radar:
            address += " (Needs radar key)"
        toilet = {
            'data_source': f'www.bexley.gov.uk, {today.strftime("%d/%m/%Y")}',
            'borough': 'Bexley',
            'address': address,
            'opening_hours': opening,
            'name': name,
            'baby_change': baby_change,
            'latitude': lat,
            'longitude': lng,
            'wheelchair': wheelchair,
            'open': True
        }
        toilets.append(toilet)
    with open("Data/processed_data_bexley.json", "w") as dataFile:
        # Need to manually add coords to this dataset because coords inaccurate
        json.dump(toilets, dataFile)


def extract_bexley_data():
    process_data(get_raw_data())


if __name__ == "__main__":
    extract_bexley_data()
