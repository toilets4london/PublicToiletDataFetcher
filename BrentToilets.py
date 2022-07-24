import requests
from bs4 import BeautifulSoup
import json
from Helpers import is_related_to_babychange, is_related_to_disabled
from datetime import date

# Difficult the get the request body because of cross site requests / cookies - Copy json from devtools manually and
# parse

BASE_URL = "https://www.brent.gov.uk/"
URL = "https://www.brent.gov.uk/services-for-residents/transport-and-streets/public-toilets/"


def get_brent_toilets():
    today = date.today()
    print("Brent toilets: [Warning] - remember to revisit url and copy json from api response body to "
          "data/brent_raw.json")
    with open("data/brent_raw.json", "r") as rawfile:
        data = json.load(rawfile)
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

