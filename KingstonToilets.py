import requests
import json
from bs4 import BeautifulSoup
from Geocoder import geocode

URL = "https://www.kingston.gov.uk/environment/public-toilets"


def get_kingston_data():
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")
    lists = soup.find_all("ul")
    car_parks = [t.find_all(text=True)[0] for t in lists[3].find_all("li")]
    parks = [t.find_all(text=True)[0] for t in lists[5].find_all("li")]
    toilets = []
    for t in car_parks:
        if "closed" in t.lower():
            continue
        name, opening_hours = t.split(": ")
        address = "Public toilet, "+name+", London borough of Kingston upon Thames"
        coords = geocode(address)
        if coords == "unavailable":
            print(address, "coordinates unavailable")
        toilets.append({
            "name": "Car park toilet",
            "address": name,
            "opening_hours": opening_hours,
            "latitude": coords[0],
            "longitude": coords[1],
            "data_source": URL,
            "borough": "Kingston upon Thames",
            "wheelchair": True
        })
    for name in parks:
        address = "Public toilet, "+name+", London borough of Kingston upon Thames"
        coords = geocode(address)
        if coords == "unavailable":
            print(address, "coordinates unavailable")
        toilets.append({
            "name": "Park toilet",
            "address": name,
            "opening_hours": "dawn - dusk daily",
            "latitude": coords[0],
            "longitude": coords[1],
            "data_source": URL,
            "borough": "Kingston upon Thames",
            "wheelchair": True
        })
    with open("Data/processed_data_kingston.json", "w") as jsonfile:
        json.dump(toilets, jsonfile)


if __name__ == '__main__':
    get_kingston_data()