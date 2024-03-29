import requests
from bs4 import BeautifulSoup
import json
import re
import Geocoder
from datetime import date


COMMUNITY_URL = "https://www.newham.gov.uk/community-parks-leisure/public-toilets-newham/2"
PUBLIC_URL = "https://www.newham.gov.uk/community-parks-leisure/public-toilets-newham/3"


def get_community_data():
    response = requests.get(COMMUNITY_URL)
    return response.text


def get_public_data():
    response = requests.get(PUBLIC_URL)
    return response.text


def parse_community(html):
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all("div", {"class": "editor"})[0]
    ps = div.find_all("p")
    ps_split = []
    for p in ps[3:len(ps)-1]:
        ps_split.append([cleanhtml(s) for s in re.split('<br/>|<br />', str(p))])
    return ps_split


def clean_address(text):
    a = re.sub(r'\n|\r|\xa0|\u200b|\t|\xa0|&nbsp;|\u202f', ' ', (text))
    a = ' '.join([part for part in a.split(' ') if part != ' ' and part != ''])
    return a

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    noescaped = re.sub(r'\n|\r|\xa0|\u200b',' ', cleantext)
    return noescaped


opening_hour_match_words = ['opening', 'times', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', ':00', 'pm', 'noon']


def is_opening_hours_related(line):
    for w in opening_hour_match_words:
        if w in line.lower():
            return True
    return False


def interpret_paragraphs(ps):
    toilets = []
    today = date.today()
    for p in ps:
        name = p[0]
        address = ''
        opening_hours = ''
        for line in p[1:len(p)]:
            if is_opening_hours_related(line):
                opening_hours += line
            else:
                address += line.replace('Hgh','High').replace('Address: ','')
        address = address.replace('  ',' ')
        if len(address) > 0:
            if address[0] == ' ':
                address = address[1:len(address)]
        latlng = Geocoder.geocode(address)
        if latlng == "unavailable":
            print(address + " Unavailable")
        else:
            toilet = {
                'data_source': f'newham.gov.uk/community-parks-leisure/public-toilets-newham/2 on {today.strftime("%d/%m/%Y")}',
                'borough': 'Newham',
                'address': address,
                'opening_hours': opening_hours,
                'name': name,
                'baby_change': True,
                'latitude': float(latlng[0]),
                'longitude': float(latlng[1]),
                'wheelchair': True,
            }
            toilets.append(toilet)
    return toilets


def extract_all_newham_toilets():
    community = get_community_data()
    parsed_community = interpret_paragraphs(parse_community(community))
    with open("Data/processed_data_newham.json", 'w') as dataFile:
        json.dump(parsed_community, dataFile)


if __name__ == "__main__":
    extract_all_newham_toilets()