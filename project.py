import PySimpleGUI as sg
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime
from geopy.geocoders import Nominatim

# Used as follows: FONT+str(<number>), <number> increases or decreases the font fize
FONT = "Montserrat "


def main():
    # Elements inside the window
    layout = [
        [sg.Text("CS50P Weather Project", size=(16, 1), font=FONT + str(20))],
        [
            sg.Text("User input field :", size=(12, 1), font=FONT + str(18)),
            sg.Input(
                "", key="Input1", size=(25, 3), enable_events=True, font=FONT + str(18)
            ),
        ],
        [
            sg.Button("Search", size=(20, 1), font=FONT + str(16)),
            sg.Button("Exit", size=(20, 1), font=FONT + str(16)),
        ],
    ]

    # Window initialization
    window = sg.Window(
        "CS50P Project", layout, element_justification="c", finalize=True
    )

    # Bind Enter key to search button
    window["Input1"].bind("<Return>", "_Enter")

    # Event loop
    while True:
        event, values = window.read()
        # If app is closed without the user entering a value

        if event == sg.WIN_CLOSED or event == "Exit":
            print("Exiting application.")
            break

        if event == "Search" or event == "Input1" + "_Enter":
            try:
                user_input = values["Input1"].strip()
                if not user_input:
                    raise ValueError
                temperature, humidity, precipitation, time = api()[0], api()[1], api()[2], get_time()
                get_coordinates(user_input)
                print(get_coordinates(capitalize(user_input))[0], get_coordinates(capitalize(user_input))[1])
                window.close()
            except ValueError:
                # Pop up window when user does not enter a value
                no_input_popup()


def no_input_popup():
    sg.popup(
        "Error", "Please enter a valid input in the search bar.", font=FONT + str(18)
    )


# TODO: Configure the API to return informations about a city. Temperature, humidity and precipitation (Might change them later on)
def api():
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

# TODO: Fix geopy
def get_coordinates(city: str):
    loc = Nominatim(user_agent="GetLoc")
 
# entering the location name
    getLoc = loc.geocode(f"{city}")

    return getLoc.latitude, getLoc.longitude


if __name__ == "__main__":
    main()
