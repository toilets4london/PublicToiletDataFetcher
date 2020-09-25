import requests
import json

OVERPASS_URL = 'https://lz4.overpass-api.de/api/interpreter'
HEADERS = {'Content-Type': 'application/xml'}


def get_data(save_to="Data/data.json", query_file="Data/query.xml"):
    with open(query_file, 'r') as query:
        xml = query.read()
    response = requests.post(
        OVERPASS_URL,
        data=xml,
        headers=HEADERS
    )
    with open(save_to, 'w') as dataFile:
        json.dump(response.json(), dataFile)


def get_broader_data():
    """ Mixed toilet data from openstreetmap including privately owned toilets"""
    save_to = "Data/mixed_data.json"
    query_file = "Data/broader_query.xml"
    get_data(save_to, query_file)

get_data()
get_broader_data()