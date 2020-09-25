import requests
import json

OVERPASS_URL = 'https://lz4.overpass-api.de/api/interpreter'
HEADERS = {'Content-Type': 'application/xml'}


def get_data(save_to="Data/data.json", query_file="Data/query.xml"):
    """ Public toilet data from openstreetmap"""
    print("Getting data from OpenStreetMap using query in %s"%query_file)
    with open(query_file, 'r') as query:
        xml = query.read()
    response = requests.post(
        OVERPASS_URL,
        data=xml,
        headers=HEADERS
    )
    print("Saving data to file %s"%save_to)
    with open(save_to, 'w') as dataFile:
        json.dump(response.json(), dataFile)


def get_broader_data():
    """ Mixed toilet data from openstreetmap including privately owned toilets"""
    save_to = "Data/mixed_data.json"
    query_file = "Data/broader_query.xml"
    get_data(save_to, query_file)
