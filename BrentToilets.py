import requests
from bs4 import BeautifulSoup
import json
from Helpers import is_related_to_babychange, is_related_to_disabled
from datetime import date

BASE_URL = "https://www.brent.gov.uk/"
URL = "https://www.brent.gov.uk/services-for-residents/transport-and-streets/public-toilets/"


def get_brent_json():
    resp = requests.post("https://www.brent.gov.uk/brent-api/search/list",
                         json={"search": "",
                               "facets": [],
                               "filter": "template_1 eq '21028f0a3c334993bc40ae9327463a46' and brent_item_has_layout and path_1/any(t:t eq '110d559fdea542ea9c1c8a5df7e70ef9')",
                               "orderBy": ["brent_item_title"],
                               "searchType": "Directory",
                               "size": 25},
                         headers={
                             "content-type": "application/json",
                             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
                         })
    return resp.json()


def get_brent_toilets():
    today = date.today()
    data = get_brent_json()
    toilets = []
    for entry in data["results"]:
        doc = entry["document"]
        toilet = {
            "name": doc["brentItemTitle"],
            "latitude": doc["brentItemGeoLocation"]["coordinates"][1],
            "longitude": doc["brentItemGeoLocation"]["coordinates"][0],
            "address": doc["brentItemAddress"],
            "open": True,
            "wheelchair": False,
            "baby_change": False,
            "data_source": f'https://www.brent.gov.uk/services-for-residents/transport-and-streets/public-toilets/ {today.strftime("%d/%m/%Y")}',
            "borough": "Brent",
            "opening_hours": ""
        }

        get_url = BASE_URL + doc["brentItemUrl"]
        response = requests.get(get_url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
        }).text
        soup = BeautifulSoup(response, 'html.parser')
        divs = soup.find_all("div", {"class": "directory directory_with-margin directory_opening-times"})
        opening_div = divs[0].find_all("div", {"class": "rich-text directory__entity"})
        text = "".join(opening_div[0].find_all(text=True))
        toilet["opening_hours"] = text.strip()
        toilet["wheelchair"] = is_related_to_disabled(response)
        toilet["baby_change"] = is_related_to_babychange(response)
        toilets.append(toilet)
    with open("data/processed_data_brent.json", "w") as f:
        json.dump(toilets, f)


if __name__ == '__main__':
    get_brent_toilets()
