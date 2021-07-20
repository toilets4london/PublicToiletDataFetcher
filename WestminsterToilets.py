import json
import requests
from pyproj import Proj, transform

url = "https://utility.arcgis.com/usrsvcs/servers/7023b128344b47acbac76fc47f471703/rest/services/WCC/AGOL/MapServer" \
      "/58/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A-20000%2C" \
      "%22ymin%22%3A5000000%2C%22xmax%22%3A-10000%2C%22ymax%22%3A7000000%2C%22spatialReference%22%3A%7B%22wkid%22" \
      "%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100 "

v84 = Proj(proj="latlong", towgs84="0,0,0", ellps="WGS84")
v36 = Proj(proj="latlong", k=0.9996012717, ellps="airy", towgs84="446.448,-125.157,542.060,0.1502,0.2470,0.8421,"
                                                                 "-20.4894")
vgrid = Proj(init="world:bng")


def ENtoLL84(easting, northing):
    """Returns (longitude, latitude) tuple - unintuitive order"""
    vlon36, vlat36 = vgrid(easting, northing, inverse=True)
    return transform(v36, v84, vlon36, vlat36)


def get_data():
    return requests.get(url).text


def get_westminster_toilets():
    raw = get_data()
    dic = json.loads(raw)
    toilets = []

    for feature in dic["features"]:
        attr = feature["attributes"]
        lng, lat = ENtoLL84(attr["Eastings"], attr["Northings"])
        toilets.append({
            'data_source': 'https://www.westminster.gov.uk/leisure-libraries-and-community/public-toilets on 20/07/2021',
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
