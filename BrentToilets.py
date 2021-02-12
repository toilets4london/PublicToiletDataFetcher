import requests
from bs4 import BeautifulSoup
import json
import re


URL = "https://www.brent.gov.uk/services-for-residents/transport-and-streets/public-toilets/"


def get_link_data():
    response = requests.get(URL)
    return response.text


def parse_main_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find(id="listing")
    items = ul.find_all("li")
    links = []
    for i in items:
        for a in i.find_all("a"):
            links.append(a['href'])
    return links


def only_single_whitespace(str):
    spl = str.replace("\n", " ").split(" ")
    arr = []
    for part in spl:
        if part != "" and part != " ":
            arr.append(part)
    return " ".join(arr)


def parse_raw_data(raw_html):
    pattern = re.compile("<span class='location'>.*?</span>")
    latlng = re.search(pattern, raw_html).group().replace("<span class='location'>", "").replace("</span>", "")
    components = latlng.split(",")
    lat = float(components[0])
    lng = float(components[1])

    toilet = {
        'data_source': 'Extracted from https://www.brent.gov.uk/services-for-residents/transport-and-streets/public-toilets/ on 12/02/2021',
        'borough': 'Brent',
        'latitude': lat,
        'longitude': lng
    }

    addr_pattern = re.compile("ddress(.*?)<p(.*?)>(.*?)<(.*?)>", re.S)
    disabled_pattern = re.compile("isabled(.*?)<p(.*?)>(.*?)<(.*?)>", re.S)
    open_hours_pattern = re.compile("ours(.*?)<p(.*?)>(.*?)<(.*?)>", re.S)
    baby_change_pattern = re.compile("aby(.*?)<p(.*?)>(.*?)<(.*?)>", re.S)
    name_pattern = re.compile("<h1(.*?)>(.*?)<(.*?)>", re.S)

    addr = re.search(addr_pattern, raw_html)
    dis = re.search(disabled_pattern, raw_html)
    open = re.search(open_hours_pattern, raw_html)
    baby = re.search(baby_change_pattern, raw_html)
    name = re.search(name_pattern, raw_html)

    if name:
        toilet['name'] = get_name(only_single_whitespace(name.group()))
    if addr:
        toilet['address'] = get_address(only_single_whitespace(addr.group()))
    if dis:
        toilet['wheelchair'] = get_is_disabled(only_single_whitespace(dis.group()))
    if open:
        toilet['opening_hours'] = get_opening_hours(only_single_whitespace(open.group()))
    if baby:
        toilet['baby_change'] = get_is_baby_change(only_single_whitespace(baby.group()))

    return toilet


def get_is_disabled(match):
    return "yes" in match.lower() or "conventional" in match.lower() or "radar" in match.lower()


def get_is_baby_change(match):
    return "yes" in match.lower() or "conventional" in match.lower()


def extract_from_p_tag(text):
    pattern = re.compile("<p>(.*?)</p>", re.S)
    t = re.search(pattern, text)
    if t:
        return t.group().replace("<p>", "").replace("</p>", "")
    else:
        return ""


def extract_from_h1_tag(text):
    pattern = re.compile("<h1>(.*?)</h1>", re.S)
    t = re.search(pattern, text)
    if t:
        return t.group().replace("<h1>", "").replace("</h1>", "")
    else:
        return ""


def get_opening_hours(match):
    return extract_from_p_tag(match)


def get_address(match):
    return extract_from_p_tag(match)


def get_name(match):
    return extract_from_h1_tag(match)


def get_all_brent_toilets():
    links = parse_main_page(get_link_data())
    toilets = []
    for link in links[0:len(links)-1]:
        data = requests.get(link).text
        toilet = parse_raw_data(data)
        toilets.append(toilet)
    with open("Data/processed_data_brent.json", 'w') as dataFile:
        json.dump(toilets, dataFile)

