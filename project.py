# Tkinter GUI  #
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image

# API #
import openmeteo_requests
import requests
import requests_cache
import pandas as pd
from retry_requests import retry
from geopy.geocoders import Nominatim


BACKGROUND_COLOR = "#426b9e"


def main():
    window = tk.Tk()
    app_gui(window)
    window.mainloop()


#   ROW >    COLUMN v
def app_gui(window):

    global user_loc_input, temperature_label, humidity_label, precipitation_label, error_label, logo_app_label

    # Window size can not be resized
    window.resizable(width=False, height=False)

    # Font
    font = "Montserrat"

    # Colors
    font_color = "#ffffff"
    details_color = "#7aa4c3"

    # Window initialization
    window.configure(bg=BACKGROUND_COLOR)
    window.geometry("415x415")
    window.title("CS50P Hunxio's Project")
    window.grid_columnconfigure(0, weight=1)

    # Icon
    icon = PhotoImage(file="logo.png")
    window.iconphoto(False, icon)

    # Text Text
    location_text = tk.Label(window, text="CS50P Weather Project", font=(font, 17))
    location_text.config(bg=BACKGROUND_COLOR, fg=font_color)
    location_text.grid(row=1, column=0, sticky="WE", padx=20, pady=10)

    # Logo App
    logo_app = PhotoImage(file="logo.png")
    logo_app.image = logo_app
    logo_app_label = tk.Label(image=logo_app)
    logo_app_label.config(bg=BACKGROUND_COLOR)
    logo_app_label.grid(row=0, column=0, sticky="N")

    # Input Field
    user_loc_input = tk.Entry(window)
    user_loc_input.grid(row=2, column=0, sticky="WE", padx=10)

    # Button Search
    confirm_button = tk.Button(text="Find the temperature", command=update_weather)
    confirm_button.config(bg=details_color, fg=font_color, font=(font, 13))
    confirm_button.grid(row=3, column=0, sticky="N", pady=10)

    # Initial Labels for Temperature, Humidity, Precipitation and Error
    temperature_label = tk.Label(
        window, text="", font=(font, 14), bg=BACKGROUND_COLOR, fg=font_color
    )

    humidity_label = tk.Label(
        window, text="", font=(font, 14), bg=BACKGROUND_COLOR, fg=font_color
    )

    precipitation_label = tk.Label(
        window, text="", font=(font, 14), bg=BACKGROUND_COLOR, fg=font_color
    )

    error_label = tk.Label(
        window, text="", font=(font, 15), bg=BACKGROUND_COLOR, fg="#ff4c4c"
    )


# Validation returns values or an error message in case of invalid inputs
def validation() -> dict | str:
    user_input = user_loc_input.get()
    if user_input:
        try:
            get_coord = get_coordinates(user_input)
            latitude, longitude = get_coord["latitude"], get_coord["longitude"]
            details = temperature_api(latitude, longitude)
            return {
                "temperature": details["temperature"],
                "humidity": details["humidity"],
                "precipitation": details["precipitation"],
            }
        except AttributeError:
            return "The desired location was not found"
    else:
        return "Please insert a location"


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


# Retrieves the user's current latitude and longitude
def get_coordinates(city: str) -> dict:
    geolocator = Nominatim(user_agent="CS50PWeather")
    getLoc = geolocator.geocode(city)

    return {"latitude": getLoc.latitude, "longitude": getLoc.longitude}


def window_update(
    temperature_update: int, humidity_update: float, precipitation_update: float
) -> None:
    # The logo image gets created once again to avoid it to disappear once the values are retrieved from the query
    logo_app = PhotoImage(file="logo.png")
    logo_app.image = logo_app
    logo_app_label = tk.Label(image=logo_app)
    logo_app_label.config(bg=BACKGROUND_COLOR)
    logo_app_label.grid(row=0, column=0, sticky="N")

    temperature_label.config(text=f"Temperature:  {temperature_update} °C")
    temperature_label.grid(row=4, column=0, sticky="WE", padx=20, pady=10)
    humidity_label.config(text=f"Humidity:  {humidity_update} %")
    humidity_label.grid(row=5, column=0, sticky="WE", padx=20, pady=10)
    precipitation_label.config(text=f"Precipitation:  {precipitation_update} %")
    precipitation_label.grid(row=6, column=0, sticky="WE", padx=20, pady=10)


# Function to update weather information
def update_weather() -> None:
    result = validation()
    if isinstance(result, dict):
        error_label.grid_forget()
        temperature = result["temperature"]
        humidity = result["humidity"]
        precipitation = result["precipitation"]
        window_update(temperature, humidity, precipitation)
    else:
        # If the result is a string, it means an error occurred, show the message
        temperature_label.grid_forget()
        humidity_label.grid_forget()
        precipitation_label.grid_forget()
        error_label.config(text=f"{result}")
        error_label.grid(row=7, column=0, sticky="WE", padx=20, pady=10)


if __name__ == "__main__":
    main()
