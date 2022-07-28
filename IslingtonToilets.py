import requests
import json
from bs4 import BeautifulSoup
from Helpers import only_single_whitespace
from Geocoder import geocode

URL = "https://www.islington.gov.uk/roads/public-toilets"


def get_islington_data():
    html = requests.get(URL).text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all("table")[0]
    rows = table.find_all("tr")
    toilets = []
    if "Chapel Market" in html:
        toilets.append({
            "name": "Chapel Market toilet",
            "latitude": 51.53378935888524,
            "longtiude": -0.10867538244253722,
            "borough": "Islington",
            "address": "15 White Conduit St, N1 9EL",
            "opening_hours": "8am to 6.30pm Monday to Saturday and 8am to 4pm on Sundays",
            "data_source": URL
        })
    for row in rows:
        cells = row.find_all("td")
        name = " ".join([only_single_whitespace(t) for t in cells[0].find_all(text=True)])
        address = " ".join([only_single_whitespace(t) for t in cells[1].find_all(text=True)])
        if "name" in name.lower():
            continue
        if "closed" in name.lower():
            continue
        coords = geocode(f"{name}, {address}")
        if coords == "unavailable":
            print("Coords unavailable for", name, address)
            continue
        toilets.append({
            "name": name,
            "latitude": coords[0],
            "longitude": coords[1],
            "borough": "Islington",
            "address": address,
            "opening_hours": "24hrs",
            "data_source": URL,
            "fee": "20p",
            "wheelchair": True
        })
    with open("Data/processed_data_islington.json", "w") as datafile:
        json.dump(toilets, datafile)


if __name__ == '__main__':
    get_islington_data()
