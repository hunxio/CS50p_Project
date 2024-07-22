# Tkinter GUI  #
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
# Integrations for API  #
from utils import get_time, get_coordinates
# API #
import openmeteo_requests
import requests
import requests_cache
import pandas as pd
from retry_requests import retry


def main():
    app_gui()


def app_gui():

    global user_loc_input

    # Font
    font = "Montserrat"
    # Colors
    background_color = "#426b9e"
    font_color = "#ffffff"
    details_color = "#7aa4c3"

    # Window initialization
    window = tk.Tk()
    window.configure(bg=background_color)
    window.geometry("350x350")
    window.title("CS50P Hunxio's Project")
    window.grid_columnconfigure(0, weight=1)

    # Icon
    icon = PhotoImage(file="logo.png")
    window.iconphoto(False, icon)

    # Text
    location_text = tk.Label(window, text="CS50P Weather Project", font=(font, 17))
    location_text.config(bg=background_color, fg=font_color)
    location_text.grid(row=1, column=0, sticky="WE", padx=20, pady=10)

    # Logo App
    logo_app = PhotoImage(file="logo.png")
    logo_app.image = logo_app
    logo_app_label = tk.Label(window, image=logo_app)
    logo_app_label.config(bg=background_color)
    logo_app_label.grid(row=0, column=0, padx=20)

    # Input Field
    user_loc_input = tk.Entry(window)
    user_loc_input.grid(row=2, column=0, sticky="WE", padx=10)

    # Button Search
    confirm_button = tk.Button(text="Find the temperature", command=input_validation)
    confirm_button.config(bg=details_color, fg=font_color, font=(font, 13))
    confirm_button.grid(row=3, column=0, sticky="N", pady=10)

    window.mainloop()

def input_validation() -> str:
    user_input = user_loc_input.get()
    if user_input:
        try:
            latitude, longitude, time = (
                get_coordinates(user_input)["latitude"],
                get_coordinates(user_input)["longitude"],
                get_time(),
            )
            details = temperature_api(latitude, longitude)
            # For the moment the results will be shown in the Terminal
            print(f"Temperature: {details["temperature"]}°C\nHumidity: {details["humidity"]}%\nPrecipitation: {details["precipitation"]}%")
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
        "latitude": user_latitude,  # Receives the latitude from get_coordinates
        "longitude": user_longitude,  # Receives the longitude from get_coordinates
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
    return {
        "temperature": round(current_temperature_2m),
        "humidity": float("%.1f" % current_relative_humidity_2m),
        "precipitation": int(current_precipitation),
    }


if __name__ == "__main__":
    main()
