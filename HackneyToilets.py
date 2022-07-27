import requests
from bs4 import BeautifulSoup
from Geocoder import geocode
import json


def get_html():
    return requests.get("https://hackney.gov.uk/streetlitter/").text


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    uls = soup.find_all("ul")
    section = uls[2]
    toilets = [t.text.replace("\xa0", " ") for t in section.find_all("li")]
    return toilets


def get_hackney_data():
    html = get_html()
    parsed = parse_html(html)
    toilets = []
    for s in parsed:
        toilet = {}
        parts = s.split(" ")
        parts = [p.replace(",", "") for p in parts]
        address = " ".join(parts[:-1])
        toilet["address"] = address
        opening_hours = parts[-1].replace("(", "").replace(")", "")
        toilet["opening_hours"] = opening_hours
        toilet["borough"] = "Hackney"
        coords = geocode("Public Toilet " + address)
        if coords == "unavailable":
            print(f"[Hackney toilets] unavailable coords for {address}")
        else:
            toilet["latitude"] = coords[0]
            toilet["longitude"] = coords[1]
        toilet["data_source"] = "hackney.gov.uk"
        toilets.append(toilet)
    with open("Data/processed_data_hackney.json", "w") as f:
        json.dump(toilets, f)


if __name__ == '__main__':
    get_hackney_data()
