import json
import itertools
import numpy as np
import matplotlib.pyplot as plt
import Geocoder

TAGS = ["access","toilets:wheelchair","disabled","note","male","opening_hours","wheelchair",
        "female","name","fee","unisex","description","changing_table"]

bfile = open("Data/boroughs.txt","r")
BOROUGHS = bfile.read().split(", ")
bfile.close()


def get_name(toilet):
    try:
        return toilet['name']
    except KeyError:
        return ""


def is_disabled(toilet):
    try:
        if toilet['disabled'] == 'yes':
            return True
        return False
    except KeyError:
        return False


def is_wheelchair_accessible(toilet):
    try:
        if toilet['wheelchair'] == 'yes':
            return True
        elif toilet['toilets:wheelchair'] == 'yes':
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


def read_json_coords(path_to_json_data="Data/data.json"):
    with open(path_to_json_data) as dataFile:
        geoData = json.loads(dataFile.read())
        elements = geoData["elements"]
        points = [(node["lat"], node["lon"]) for node in elements]
    return points


def load_all_json(path):
    with open(path) as datafile:
        d = json.loads(datafile.read())
    return d


def count_occurances_of_tag(nodes, tag):
    tot = 0
    for node in nodes:
        try:
            v = node['tags'][tag]
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


def plot_tags(path):
    tags_info = explore_tags(path)
    height = tags_info['occurrences']
    bars = tags_info['tags']
    y_pos = np.arange(len(bars))
    # Create bars
    plt.bar(y_pos, height)
    # Create names on the x-axis
    plt.xticks(y_pos, bars)
    # Show graphic
    plt.show()


def clean_dict(dict, tags):
    return {k: v for k, v in dict.items() if (k in tags)}


def get_borough(address):
    for b in BOROUGHS:
        if b in address:
            return b
    return ""


def filter_json_data():
    with open("Data/locations.txt",'r') as locs:
        locations = locs.read().split("\n")
        wcs = []
        dict = load_all_json("Data/data.json")
        toilets = dict['elements']
        for i, t in enumerate(toilets):
            toilet_tags = t['tags']
            filtered_dict = {}
            filtered_dict['address'] = locations[i]
            filtered_dict['latitude'] = t['lat']
            filtered_dict['longitude'] = t['lon']
            filtered_dict['borough'] = get_borough(locations[i])
            filtered_dict['disabled'] = is_disabled(toilet_tags)
            filtered_dict['wheelchair'] = is_wheelchair_accessible(toilet_tags)
            filtered_dict['name'] = get_name(toilet_tags)
            filtered_dict['opening_hours'] = get_hours(toilet_tags)
            wcs.append(filtered_dict)
    return wcs


def write_filtered_json_osm(newpath):
    new_toilets = filter_json_data()
    with open(newpath, 'w') as dataFile:
        json.dump(new_toilets, dataFile)

write_filtered_json_osm("Data/filtered_data.json")




