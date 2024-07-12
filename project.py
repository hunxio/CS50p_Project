import PySimpleGUI as sg
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry


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
                print(api())
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
    # Openmeteo API request
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_precipitation = current.Variables(2).Value()
    return (
        f"Current time {current.Time()}\nCurrent temperature_2m {current_temperature_2m}\nCurrent relative_humidity_2m {current_relative_humidity_2m}\nCurrent precipitation {current_precipitation}"
    )

#TODO: Time to show hh:mm format
def time_format(time):
    ...



if __name__ == "__main__":
    main()
