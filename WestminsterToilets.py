import json
import requests
from Helpers import ENtoLL84
from datetime import date

url = "https://utility.arcgis.com/usrsvcs/servers/7023b128344b47acbac76fc47f471703/rest/services/WCC/AGOL/MapServer" \
      "/58/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A-20000%2C" \
      "%22ymin%22%3A5000000%2C%22xmax%22%3A-10000%2C%22ymax%22%3A7000000%2C%22spatialReference%22%3A%7B%22wkid%22" \
      "%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100 "


def get_data():
    return requests.get(url).text


def get_westminster_toilets():
    today = date.today()
    raw = get_data()
    dic = json.loads(raw)
    toilets = []

    for feature in dic["features"]:
        attr = feature["attributes"]
        lng, lat = ENtoLL84(attr["Eastings"], attr["Northings"])
        toilets.append({
            'data_source': f'westminster.gov.uk/leisure-libraries-and-community/public-toilets {today.strftime("%d/%m/%Y")}',
            'borough': 'Westminster',
            'address': attr["Location"] + " " + attr["Postcode"],
            'opening_hours': attr.get("Opening_Times", "") or "",
            'name': attr["Site_Type"] + " " + attr["Site_Name"],
            'baby_change': "baby" in str(attr.get("Facilities", "")).lower(),
            'latitude': lat,
            'longitude': lng,
            'wheelchair': "y" in str(attr.get("Wheelchair_YN", "")).lower(),
            'open': True
        })
        with open("Data/westminster_data.json", "w") as dataFile:
            json.dump(toilets, dataFile)


if __name__ == "__main__":
    get_westminster_toilets()
