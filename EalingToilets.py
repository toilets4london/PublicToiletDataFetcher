import requests
from bs4 import BeautifulSoup
import json
from datetime import date


URL = "https://www.ealing.gov.uk/info/201153/street_care_and_cleaning/200/public_toilets/4"


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('tbody')
    rows = []
    for t in tables:
        rs = t.find_all('tr')
        for i, r in enumerate(rs):
            if i > 0:
                rows.append([[b.replace("*"," ") for b in c.text.replace(" ","*").split()] for c in r.find_all('td')])
    return rows


def html_to_toilets(html):
    """
    Requires filling in lat long manually
    """
    today = date.today()
    rows = parse(html)[1:]
    toilets = []
    for r in rows:
        t = {}
        t['name'] = 'Community Toilet'
        t['address'] = r[0][0]
        t['opening_hours'] = " ".join(r[0][1:])
        t['wheelchair'] = ('Y' in r[1][0].upper())
        t['baby_change'] = ('Y' in r[2][0].upper())
        t['data_source'] = f'ealing.gov.uk {today.strftime("%d/%m/%Y")}'
        t['borough'] = 'Ealing'
        t['latitude'] = 0
        t['longitude'] = 0
        toilets.append(t)
    return toilets


def get_ealing_data():
    data = requests.get(URL, verify=False).text
    ts = html_to_toilets(data)
    with open('Data/processed_data_ealing.json', 'w') as dataFile:
        json.dump(ts, dataFile)


if __name__ == "__main__":
    get_ealing_data()