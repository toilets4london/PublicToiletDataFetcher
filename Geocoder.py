from geopy.geocoders import Nominatim


def geocode(location_name):
    try:
        geolocator = Nominatim(user_agent="name")
        location = geolocator.geocode(location_name)
        return location.latitude, location.longitude
    except:
        return "unavailable"


def reverse_geocode(lat,long):
    geolocator = Nominatim(user_agent="name")
    location = geolocator.reverse("%s, %s"%(str(lat),str(long)))
    return location.address

