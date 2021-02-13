import requests
import json
from HillingdonToilets import ENtoLL84

URL = "https://my.haringey.gov.uk/GetOWS.ashx?VERSION=1.0.0&SERVICE=WFS&REQUEST=GetFeature&TYPENAME=Toilets&MAPSOURCE=mapsources%2FAllMaps&OUTPUTFORMAT=GeoJSON_BBOX"



def get_haringey_data():
    data = requests.get(URL).text
    toilet_data = json.loads(data)[0]['features']

    toilets = []

    for toilet in toilet_data:
        bbox = toilet['geometry']['coordinates']
        info = toilet['properties']['fields']

        name = info['toilet']
        address = info['location']
        disabled = 'y' in info['disabled_access'].lower()
        opening = info['opening_times']
        lng, lat = ENtoLL84(bbox[0][0], bbox[0][1])

        processed_toilet = {
            'data_source': 'Data extracted from https://www.haringey.gov.uk/parking-roads-and-travel/roads-and-streets/public-toilets/map-public-toilets-haringey on 13/02/21',
            'borough': 'Haringey',
            'address': address,
            'opening_hours': opening,
            'name': name,
            'latitude': lat,
            'longitude': lng,
            'wheelchair': disabled
        }

        toilets.append(processed_toilet)

    with open("Data/processed_data_haringey.json", "w") as dataFile:
        json.dump(toilets, dataFile)


