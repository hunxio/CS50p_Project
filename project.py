from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import openmeteo_requests
import requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime
from geopy.geocoders import Nominatim


# Used as follows: FONT+str(<number>), <number> increases or decreases the font fize
FONT = "Montserrat"
BACKGROUND_COLOR = "#426b9e"
FONT_COLOR = "#ffffff"
DETAILS_COLOR = "#7aa4c3"


def main():
    global user_loc_input
    # Window initialization
    window = tk.Tk()
    window.configure(bg=BACKGROUND_COLOR)
    window.geometry("325x325")
    window.title("CS50P Hunxio's Project")
    window.grid_columnconfigure(0, weight=1)

    # Icon
    icon = PhotoImage(file="logo.png")
    window.iconphoto(False, icon)

    # Text
    location_text = tk.Label(window, text="CS50P Weather Project", font=(FONT, 15))
    location_text.config(bg=BACKGROUND_COLOR, fg=FONT_COLOR)
    location_text.grid(row=1, column=0, sticky="WE", padx=20, pady=10)

    # Logo App
    logo_app = PhotoImage(file="logo.png")
    logo_app.image = logo_app
    logo_app_label = tk.Label(window, image=logo_app)
    logo_app_label.config(bg=BACKGROUND_COLOR)
    logo_app_label.grid(row=0, column=0, padx=20)

    # Input Field
    user_loc_input = tk.Entry(window)
    user_loc_input.grid(row=2, column=0, sticky="WE", padx=10)

    # Button Search
    confirm_button = tk.Button(text="Find the temperature", command=input_validation)
    confirm_button.config(bg=DETAILS_COLOR, fg=FONT_COLOR, font=(FONT, 13))
    confirm_button.grid(row=3, column=0, sticky="N", pady=10)

    window.mainloop()


def input_validation() -> str:
    user_input = user_loc_input.get()
    if user_input:
        try:
            latitude, longitude, time = (
                get_coordinates(user_input)[0],
                get_coordinates(user_input)[1],
                get_time(),
            )
            details = temperature_api(latitude, longitude)
            print(details, time)
        except AttributeError:
            print("Invalid input")

    else:
        print("The search bar is empty, please enter your search")


def temperature_api(user_latitude: float, user_longitude: float) -> dict:
    # Cache the requests to improve performance and reduce the number of API calls.
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Openmeteo API request
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": user_latitude,  # needs to change based on location
        "longitude": user_longitude,  # needs to change based on location
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_precipitation = current.Variables(2).Value()

    # Temperature value could be 1-2 degrees different because of the rounding error
    return (
        round(current_temperature_2m),
        float("%.1f" % current_relative_humidity_2m),
        int(current_precipitation),
    )


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

    return getLoc.latitude, getLoc.longitude


if __name__ == "__main__":
    main()
