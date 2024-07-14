from tkinter import *
import tkinter as tk
import openmeteo_requests
import requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime
from geopy.geocoders import Nominatim


# Used as follows: FONT+str(<number>), <number> increases or decreases the font fize
FONT = "Montserrat"


def main():
    global user_loc_input
    # Window initialization
    window = tk.Tk()
    
    window.geometry("500x300")
    window.title("CS50P Weather Project")
    window.grid_columnconfigure(0, weight=1)

    location_text = tk.Label(window,
                         text="Please select a location",
                         font=(FONT, 15))
    location_text.grid(row=0, column=0, sticky="WE", padx=20, pady=10)

    user_loc_input = tk.Entry(window)
    user_loc_input.grid(row=1, column=0, sticky="WE", padx=10)

    confirm_button = tk.Button(text="Find the temperature", command=input_validation)
    confirm_button.grid(row=2, column=0, sticky="N", pady=10)

    window.mainloop()

def input_validation() -> str:
    user_input = user_loc_input.get()
    if user_input:
        try:
            get_coordinates(user_input)
        except AttributeError:
            print("Invalid input")
    
        
    else:
        print("The search bar is empty, please enter your search")

def temperature_api(lat, long) -> dict:
    # Cache the requests to improve performance and reduce the number of API calls.
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Openmeteo API request
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 55.7522, # needs to change based on location
        "longitude": 37.6156, # needs to change based on location
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_precipitation = current.Variables(2).Value()

    return current_temperature_2m, current_relative_humidity_2m, current_precipitation


# Get time from user's location
def get_time():
    c = datetime.now()
    current_time = c.strftime("%H:%M")
    return current_time


def get_coordinates(city: str) -> dict:
    geolocator = Nominatim(user_agent="CS50PWeather")
    getLoc = geolocator.geocode(city)
    
    return getLoc.latitude, getLoc.longitude


if __name__ == "__main__":
    main()
