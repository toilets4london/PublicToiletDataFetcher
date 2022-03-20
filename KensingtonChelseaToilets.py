import requests
from bs4 import BeautifulSoup
import json
from datetime import date


KENSINGTON_CHELSEA_URL = "https://www.rbkc.gov.uk/environment/environmental-health/public-toilets"


def get_data():
    response = requests.get(KENSINGTON_CHELSEA_URL)
    return response.text


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    rows = []
    for t in tables:
        rs = t.find_all('tr')
        for i, r in enumerate(rs):
            if i > 0:
                rows.append([c.text for c in r.find_all('td')])
    return rows


def kensington_data_to_json():
    today = date.today()
    data = get_data()
    parsed = parse(data)
    with open('Data/processed_data_kensington.json', 'w') as dataFile:
        toilets = []
        for toilet in parsed:
            t = {}
            t['name'] = 'Public Toilet'
            t['address'] = toilet[0]
            t['opening_hours'] = toilet[1]
            t['wheelchair'] = ('Y' in toilet[2].upper())
            t['baby_change'] = ('Y' in toilet[3].upper())
            t['data_source'] = f'rbkc.gov.uk/environment/environmental-health/public-toilets {today.strftime("%d/%m/%Y")}'
            t['borough'] = 'Kensington and Chelsea'
            t['latitude'] = 0
            t['longitude'] = 0
            toilets.append(t)

        json.dump(toilets, dataFile)


if __name__ == "__main__":
    kensington_data_to_json()
