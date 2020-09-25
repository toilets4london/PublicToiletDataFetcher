from geopy.geocoders import Nominatim


def geocode(location_name):
    geolocator = Nominatim(user_agent="GeoStuff")
    location = geolocator.geocode(location_name)
    return location.latitude, location.longitude


def reverse_geocode(lat,long):
    geolocator = Nominatim(user_agent="GeoStuff")
    return geolocator.reverse("%s, %s"%(str(lat),str(long)))