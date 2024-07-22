from geopy.geocoders import Nominatim


# Retrieves the user's current latitude and longitude
def get_coordinates(city: str) -> dict:
    geolocator = Nominatim(user_agent="CS50PWeather")
    getLoc = geolocator.geocode(city)

    return {
        "latitude": getLoc.latitude, 
        "longitude": getLoc.longitude
        }

