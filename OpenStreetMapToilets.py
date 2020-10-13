import itertools
import Geocoder
import requests
import json

OVERPASS_URL = 'https://lz4.overpass-api.de/api/interpreter'
HEADERS = {'Content-Type': 'application/xml'}

# Tags used on OpenStreetMap toilets
TAGS = ["access",
        "toilets:wheelchair",
        "disabled",
        "note",
        "male",
        "opening_hours",
        "wheelchair",
        "female",
        "name",
        "fee",
        "unisex",
        "description",
        "changing_table"]

bfile = open("Data/boroughs.txt","r")
BOROUGHS = bfile.read().split(", ")
bfile.close()


def get_openstreetmap_data(save_to="Data/data.json", query_file="Data/query.xml"):
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
    get_openstreetmap_data(save_to, query_file)

def get_name(toilet):
    try:
        return toilet['name']
    except KeyError:
        return ""


def is_wheelchair_accessible(toilet):
    try:
        if toilet['wheelchair'] == 'yes':
            return True
        elif toilet['disabled'] == 'yes':
            return True
        elif toilet['toilets:wheelchair'] == 'yes':
            return True
        elif toilet['wheelchair:description']:
            return True
        else:
            return False
    except KeyError:
        return False


def get_hours(toilet):
    try:
        return toilet['opening_hours']
    except KeyError:
        return ""


def get_baby_change(tags):
    try:
        if tags['changing_table'] == 'yes':
            return True
        else:
            return False
    except KeyError:
        return False

def load_all_json(path):
    with open(path) as datafile:
        d = json.loads(datafile.read())
    return d


def count_occurances_of_tag(nodes, tag):
    tot = 0
    for node in nodes:
        try:
            _ = node['tags'][tag]
            tot += 1
        except KeyError:
            pass
    return tot


def explore_tags(path):
    dic = load_all_json(path)
    nodes = dic['elements']
    keys = set(itertools.chain.from_iterable([node.keys() for node in nodes]))
    tags = set(itertools.chain.from_iterable([node['tags'].keys() for node in nodes]))
    print("Top level keys \n")
    [print(k) for k in keys]
    print("\nTags\n")
    total_number = len(nodes)
    [print("%s, %d times out of %d"%(t,count_occurances_of_tag(nodes,t),total_number)) for t in tags]
    return {"tags": tags, "occurrences": [count_occurances_of_tag(nodes, t) for t in tags]}


def get_borough(address):
    for b in BOROUGHS:
        if b in address:
            return b
    return ""


def filter_json_data():

    """Return a new list of dicts with cleaned and filtered data to match input into toilets4london backend"""

    wcs = []
    dict = load_all_json("Data/data.json")
    toilets = dict['elements']

    for t in toilets:
        toilet_tags = t['tags']
        filtered_dict = {}
        address = Geocoder.reverse_geocode(t['lat'],t['lon'])
        filtered_dict['address'] = address
        filtered_dict['latitude'] = t['lat']
        filtered_dict['longitude'] = t['lon']
        filtered_dict['borough'] = get_borough(address)
        filtered_dict['wheelchair'] = is_wheelchair_accessible(toilet_tags)
        filtered_dict['name'] = get_name(toilet_tags)
        filtered_dict['opening_hours'] = get_hours(toilet_tags)
        filtered_dict['baby_change'] = get_baby_change(toilet_tags)
        wcs.append(filtered_dict)

    return wcs


def write_filtered_json(newpath="Data/processed_data.json"):

    new_toilets = filter_json_data()

    with open(newpath, 'w') as dataFile:
        json.dump(new_toilets, dataFile)

