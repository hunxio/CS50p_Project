from datetime import datetime
from geopy.geocoders import Nominatim

# Get time from user's location, it does not show the location time
# It won't be used for the API, only "decoration"
def get_time() -> str:
    c = datetime.now()
    current_time = c.strftime("%H:%M")
    return str(current_time)


# Retrieves the user's current latitude and longitude
def get_coordinates(city: str) -> dict:
    geolocator = Nominatim(user_agent="CS50PWeather")
    getLoc = geolocator.geocode(city)

    return {
        "latitude": getLoc.latitude, 
        "longitude": getLoc.longitude
        }

