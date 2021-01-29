import requests
from bs4 import BeautifulSoup
import json
import re
import Geocoder


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


def parse_public(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all("tbody")[0]
    rows = table.find_all("tr")
    toilets = []
    for r in rows:
        cols = r.find_all("td")
        toilet_location = clean_address(''.join(cols[0].find_all(text=True)))
        postcode = clean_address(''.join(cols[1].find_all(text=True)))
        disabled = 'y' in ''.join(cols[2].find_all(text=True)).lower()
        latlng = Geocoder.geocode(toilet_location + ' '+postcode)
        if latlng != "unavailable":
            toilet = {
                'data_source': 'Extracted from https://www.newham.gov.uk/community-parks-leisure/public-toilets-newham/3 on 29/01/2021',
                'borough': 'Newham',
                'address': toilet_location + ' '+postcode,
                'opening_hours': '',
                'name': 'Public Toilet',
                'baby_change': False,
                'latitude': float(latlng[0]),
                'longitude': float(latlng[1]),
                'wheelchair': disabled
            }
            toilets.append(toilet)
        else:
            latlng = Geocoder.geocode(postcode)
            if latlng != "unavailable":
                toilet = {
                    'data_source': 'Extracted from https://www.newham.gov.uk/community-parks-leisure/public-toilets-newham/3 on 29/01/2021',
                    'borough': 'Newham',
                    'address': toilet_location + ' ' + postcode,
                    'opening_hours': '',
                    'name': 'Public Toilet',
                    'baby_change': False,
                    'latitude': float(latlng[0]),
                    'longitude': float(latlng[1]),
                    'wheelchair': disabled
                }
                toilets.append(toilet)
            else:
                print("Could not find coordinates!")
    return toilets


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
                'data_source': 'Extracted from https://www.newham.gov.uk/community-parks-leisure/public-toilets-newham/2 on 29/01/2021',
                'borough': 'Newham',
                'address': address,
                'opening_hours': opening_hours,
                'name': name,
                'baby_change': True,
                'latitude': float(latlng[0]),
                'longitude': float(latlng[1]),
                'wheelchair': True,
                'covid': "Many community toilets have been affected by Covid restrictions and may not be currently operating"
            }
            toilets.append(toilet)
    return toilets


def extract_all_newham_toilets():
    public = get_public_data()
    community = get_community_data()
    parsed_public = parse_public(public)
    parsed_community = interpret_paragraphs(parse_community(community))
    all = parsed_community+parsed_public
    print("Extracted "+str(len(all))+" toilets from Newham website")
    with open("Data/processed_data_newham.json", 'w') as dataFile:
        json.dump(all, dataFile)