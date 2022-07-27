import requests
from bs4 import BeautifulSoup
import json
from WalthamForestToilets import lat_lng_from_google_maps_url
from Helpers import is_related_to_opening, only_single_whitespace
import re

def split(text):
    return re.split(r'–|,', text)


def get_html():
    return requests.get("https://www.havering.gov.uk/info/20096/community/822/public_toilet_facilities_in_havering").text


def parse_save_toilets(html):
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find_all("ul")
    toilet_links = ul[-5].find_all("li")
    toilets = []
    for t in toilet_links:
        url = t.find_all("a")[0]
        lat, lng = lat_lng_from_google_maps_url(url["href"])
        descr = t.text.replace("\t", "").replace("\n", "").replace("\r", "")
        parts = split(descr)
        name = parts[0].replace("–", "").replace(" ", " ")
        name1 = name.split("(")[0]
        opening_hours = ""
        address = ""
        for p in parts[1:]:
            if is_related_to_opening(p):
                opening_hours += p
            else:
                address += p
        address = address.replace("–", "").replace(" ", " ")
        toilets.append({
            "name": name1.strip(),
            "address": only_single_whitespace(name + " " + address).strip(),
            "latitude": lat,
            "longitude": lng,
            "opening_hours": opening_hours.replace("–", "").replace(" ", " ").strip(),
            "data_source": "www.havering.gov.uk/info/20096/community/822/public_toilet_facilities_in_havering",
            "borough": "Havering"
        })
    with open("Data/processed_data_havering.json", "w") as jsonfile:
        json.dump(toilets, jsonfile)


def get_havering_toilets():
    toilets = get_html()
    parse_save_toilets(toilets)


if __name__ == '__main__':
    get_havering_toilets()
