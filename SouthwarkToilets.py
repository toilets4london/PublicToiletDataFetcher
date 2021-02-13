import requests
import json
from HillingdonToilets import ENtoLL84


URL = "https://geo.southwark.gov.uk/connect/analyst/controller/connectProxy/rest/Spatial/FeatureService"
Q = 'url=tables/features.json?q=SELECT * FROM "/NamedMaps/NamedTables/Public toilets in Southwark"&encodeSpecialChars=true&pageLength=1000'


def get_southwark_data():
    raw_data = requests.post(URL, Q, verify=False, headers={"Content-Type": "application/x-www-form-urlencoded"}).text

    print(raw_data)
    toilet_data = json.loads(raw_data)['features']

    toilets = []

    for toilet in toilet_data:
        info = toilet['properties']

        name = info['Name']
        address = info['Location']
        disabled = 'y' in info['DisabledFacilities'].lower()
        opening = info['OpeningTime']
        lng, lat = ENtoLL84(info['Easting'], info['Northing'])
        fee = info['CostCharge']
        babychange = 'y' in info['BabyChangingFacilities'].lower()

        processed_toilet = {
            'data_source': 'Data extracted from https://www.southwark.gov.uk/environment/public-toilets on 13/02/21',
            'borough': 'Southwark',
            'address': address,
            'opening_hours': opening,
            'name': name,
            'latitude': lat,
            'longitude': lng,
            'wheelchair': disabled,
            'fee': fee,
            'baby_change': babychange
        }

        toilets.append(processed_toilet)

    with open("Data/processed_data_southwark.json", "w") as dataFile:
        json.dump(toilets, dataFile)

