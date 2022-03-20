from enum import Enum
import requests
import json
from Helpers import ENtoLL84
from datetime import date

BASE = "https://www.mapping.cityoflondon.gov.uk/arcgis/rest/services/COMPASS_City_and_Community_Toilets/MapServer"


class CityToiletType(Enum):
    AUTOMATIC = 0
    URILIFT = 1
    COMMUNITY = 2


def make_city_url(toilet_type: CityToiletType):
    main_url = f"{BASE}/{toilet_type.value}/query?"
    query = "f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A-10000000%2C" \
            "%22ymin%22%3A-10000000%2C%22xmax%22%3A100000000%2C%22ymax%22%3A100000000%2C%22spatialReference%22%3A%7B" \
            "%22wkid%22%3A27700%7D%7D&geometryType=esriGeometryEnvelope&inSR=277000&outFields=*&outSR=277000 "
    return main_url + query


def data_to_toilet_dict(text_data):
    today = date.today()
    d = json.loads(text_data)
    features = d["features"]
    lst = []
    for f in features:
        attrs = f["attributes"]
        lng, lat = ENtoLL84(f["geometry"]["x"], f["geometry"]["y"])
        lst.append({
            "data_source": f'mapping.cityoflondon.gov.uk/ {today.strftime("%d/%m/%Y")}',
            "borough": "City of London",
            "address": attrs["ADDRESS"],
            "name": attrs["NAME"],
            "opening_hours": f"{'Mon-Fri 'if 'MON' not in attrs['OPEN_MONDAY_TO_FRIDAY'] else ''}{attrs['OPEN_MONDAY_TO_FRIDAY']}, Sat {attrs['OPEN_SATURDAY']}, Sun {attrs['OPEN_SUNDAY']}, Bank holiday {attrs['OPEN_BANK_HOLIDAY']}",
            "latitude": lat,
            "longitude": lng,
            "wheelchair": "y" in str(attrs["ACCESSIBLE_TOILETS"]).lower(),
            "baby_change": "y" in str(attrs["BABY_CHANGING_FACILITIES"]).lower(),
            "fee": "50p" if "50p" in str(attrs["NOTES"]) else ""
        })
    return lst


def get_city_toilets():
    automatic = requests.get(make_city_url(CityToiletType.AUTOMATIC)).text
    community = requests.get(make_city_url(CityToiletType.COMMUNITY)).text
    all_data = data_to_toilet_dict(automatic) + data_to_toilet_dict(community)
    with open("Data/processed_data_city.json", "w") as jsonFile:
        json.dump(all_data, jsonFile)


if __name__ == "__main__":
    get_city_toilets()