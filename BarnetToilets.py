import requests
from bs4 import BeautifulSoup
import json


# The lat / lng coordinates here are extremely inaccurate - this script needs manual entering of coordinates


BASE_URL = "https://www.barnet.gov.uk"
BARNET_URL = "https://www.barnet.gov.uk/directories/public-conveniences?keywords=&sort_by=title&page="



def get_barnet_main_page():
    urls = []
    for page in range(2):
        response = requests.get(BARNET_URL+str(page))
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all("li", {"class": "result"})
        for l in listings:
            links = l.find_all("a",href=True)
            urls += links
    urls = [BASE_URL+u['href'] for u in urls]
    return urls

def parse_barnet_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    s = soup.find(id="map_json")
    if s:
        s = ''.join(s.find_all(text=True))
        j = json.loads(s)[0]
        toilet = {
            'data_source': 'Extracted from https://www.barnet.gov.uk/directories/public-conveniences on 30/01/2021',
            'borough': 'Barnet',
            'address': j['title']+' '+j['address'][0],
            'opening_hours': '',
            'name': j['title'].split(',')[0],
            'baby_change': False,
            'latitude': float(j['latitude']),
            'longitude': float(j['longitude']),
            'wheelchair': False
        }
        return toilet
    return None


def get_all_barnet_toilets():
    urls = get_barnet_main_page()
    toilets = []
    for url in urls:
        t = parse_barnet_page(url)
        if t:
            toilets.append(t)
    with open("Data/processed_data_barnet.json", 'w') as dataFile:
        json.dump(toilets, dataFile)
