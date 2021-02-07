import json
from pyproj import Proj, transform

# E/N to lat/lng code from https://webscraping.com/blog/Converting-UK-Easting-Northing-coordinates/

v84 = Proj(proj="latlong", towgs84="0,0,0", ellps="WGS84")
v36 = Proj(proj="latlong", k=0.9996012717, ellps="airy", towgs84="446.448,-125.157,542.060,0.1502,0.2470,0.8421,"
                                                                 "-20.4894")
vgrid = Proj(init="world:bng")


def ENtoLL84(easting, northing):
    """Returns (longitude, latitude) tuple - unintuitive order"""
    vlon36, vlat36 = vgrid(easting, northing, inverse=True)
    return transform(v36, v84, vlon36, vlat36)


def westminster_csv_to_json():
    """  Data copied from https://lbhf.maps.arcgis.com/apps/webappviewer/index.html?id
    =ef1a81e22b994061981a2eb45d4c7c0b """
    with open("Data/westminster_raw.csv", "r", newline="\n") as f:
        lines = f.readlines()
    toilets = []
    lines = [line.split("\t") for line in lines]

    for l in lines:
        lng, lat = ENtoLL84(int(l[5]), int(l[6]))
        toilet = {
            'data_source': 'Copied from https://lbhf.maps.arcgis.com/apps/webappviewer/index.html?id'
                           '=ef1a81e22b994061981a2eb45d4c7c0b on 07/02/2021',
            'borough': 'Westminster',
            'address': l[2].replace(" Public Convenience",""),
            'opening_hours': "",
            'name': l[2],
            'baby_change': False,
            'latitude': lat,
            'longitude': lng,
            'wheelchair': False,
            'open': True
        }
        toilets.append(toilet)
    with open("Data/westminster_data.json", "w") as dataFile:
        json.dump(toilets, dataFile)
