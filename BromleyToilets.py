import requests
from bs4 import BeautifulSoup
import json


MAIN_URL = "https://www.bromley.gov.uk/directory/36/community_and_public_toilets/category/525"
BASE_URL = "https://www.bromley.gov.uk"


def get_data():
    response = requests.get(MAIN_URL)
    return response.text


def parse_main_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all("div", {"class": "cate_info"})
    lists = divs[0].find_all("ul")
    all_links = []
    for ul in lists:
        entries = ul.find_all("li")
        for li in entries:
            links = li.find_all("a")
            all_links += links
    link_list = [link['href'] for link in all_links]
    print(link_list)
    return link_list


def parse_detail_page(url):
    raw_data = requests.get(url).text
    soup = BeautifulSoup(raw_data, 'html.parser')
    main_content = soup.find(id="main-content")

    name = main_content.find_all("h1")[0]
    name = ''.join(name.find_all(text=True))

    table = main_content.find_all("table")[0]
    rows = table.find_all("tr")

    description = ""
    address = ""
    postcode = ""
    opening = ""
    facilities_description = ""
    lat_lng = [0, 0]

    for r in rows:
        row_name = r.find_all("th")[0]
        row_name = "".join(row_name.find_all(text=True)).lower()
        if "description" in row_name:
            description = r.find_all("td")[0]
            description = ''.join(description.find_all(text=True))
        if "address" in row_name:
            address = r.find_all("td")[0]
            address = ''.join(address.find_all(text=True))
        if "postcode" in row_name:
            postcode = r.find_all("td")[0]
            postcode = ''.join(postcode.find_all(text=True))
        if "opening" in row_name:
            opening = r.find_all("td")[0]
            opening = ''.join(opening.find_all(text=True))
        if "facilities" in row_name:
            facilities_description = r.find_all("td")[0]
            facilities_description = ''.join(facilities_description.find_all(text=True))
        if "map" in row_name:
            lat_lng = r.find_all("td")[0].find_all("input")[2]['value'].split(",")

    disabled = check_disabled(facilities_description)
    baby_change = check_baby_change(facilities_description)

    toilet = {
        'data_source': 'bromley.gov.uk on 10/08/2021',
        'borough': 'Bromley',
        'address': clean_text(address+" "+postcode),
        'opening_hours': clean_text(opening),
        'name': clean_text(name+" "+description),
        'baby_change': baby_change,
        'latitude': float(lat_lng[0]),
        'longitude': float(lat_lng[1]),
        'wheelchair': disabled,
    }
    print(toilet)
    return toilet


def create_toilet_list():
    links = parse_main_page(get_data())
    lst = []
    for link in links:
        try:
            t = parse_detail_page(BASE_URL + link)
            lst.append(t)
        except IndexError:
            print(f"Error at {BASE_URL + link}")
    return lst


def extract_bromley_json():
    toilet_list = create_toilet_list()
    with open("Data/processed_data_bromley.json", 'w') as dataFile:
        json.dump([t for t in toilet_list if t['latitude'] != 0], dataFile)


def clean_text(text):
    no_newlines = text.replace('\n',' ')
    return ' '.join(no_newlines.split())


def check_disabled(text):
    lower_case = text.lower()
    matches = ["disabled", "wheelchair", "accessible"]
    for m in matches:
        if m in lower_case:
            return True
    return False


def check_baby_change(text):
    lower_case = text.lower()
    matches = ["baby", "change", "changing"]
    for m in matches:
        if m in lower_case:
            return True
    return False



