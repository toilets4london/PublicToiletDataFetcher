from geopy.geocoders import Nominatim
import googlemaps
from os.path import exists

def get_google_api_key():
    if not exists("api_key.txt"):
        return None
    with open("api_key.txt", "r") as apikeyfile:
        key = apikeyfile.read()
        if key.strip() == "":
            return None
        return key


def geocode(location_name):
    api_key = get_google_api_key()
    if api_key == None:
        try:
            geolocator = Nominatim(user_agent="name")
            location = geolocator.geocode(location_name)
            return location.latitude, location.longitude
        except:
            return "unavailable"
    else:
        try:
            gmaps = googlemaps.Client(key=api_key)
            geocode_result = gmaps.geocode(location_name)
            lat_lng = geocode_result[0]["geometry"]["location"]
            return lat_lng["lat"], lat_lng["lng"]
        except:
            return "unavailable"



def reverse_geocode(lat,long):
    geolocator = Nominatim(user_agent="name")
    location = geolocator.reverse("%s, %s"%(str(lat),str(long)))
    return location.address

