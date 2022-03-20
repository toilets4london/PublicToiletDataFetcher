import requests
from bs4 import BeautifulSoup
import json
import Geocoder
from datetime import date

URL = "https://new.enfield.gov.uk/services/leisure-and-culture/community-toilet-scheme/"


def get_data():
    return requests.get(URL).text


def clean(text):
    nonw = " ".join([part for part in text.split() if part != ""])
    newstr = ""
    for i, letter in enumerate(nonw):
        if (letter.isupper() or letter.isnumeric()) and (nonw[max(i - 1, 0)].islower()):
            newstr += " "
        newstr += letter
    return newstr


def get_rows(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = [[clean(cell.text) for cell in r.find_all('td')] for r in soup.find_all('tr')]
    return rows


def enfield_data_to_json():
    data = get_data()
    rows = get_rows(data)[1:]
    today = date.today()
    with open('Data/processed_data_enfield.json', 'w') as dataFile:
        toilets = []
        for toilet in rows:
            t = {}
            t['name'] = 'Community Toilet'
            t['address'] = toilet[0]
            t['opening_hours'] = toilet[1]
            t['data_source'] = f'https://new.enfield.gov.uk/services/leisure-and-culture/community-toilet-scheme/ {today.strftime("%d/%m/%Y")}'
            t['borough'] = 'Enfield'
            ll = Geocoder.geocode(toilet[0])
            if ll != "unavailable":
                t['latitude'] = ll[0]
                t['longitude'] = ll[1]
            else:
                t['latitude'] = 0
                t['longitude'] = 0
            toilets.append(t)
        json.dump(toilets, dataFile)


if __name__ == "__main__":
    enfield_data_to_json()