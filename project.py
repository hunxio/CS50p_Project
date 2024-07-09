import PySimpleGUI as sg

# Used as follows: FONT+str(<number>), <number> increases or decreases the font fize
FONT = "Montserrat "

def main():
    # Elements inside the window
    layout = [
        [sg.Text("CS50P Weather Project", size=(16, 1), font=FONT+str(20))],
        [sg.Text("User input field :", size=(12, 1), font=FONT+str(18)), sg.Input("", key="Input1", size=(47,3))],
        [sg.Button("Search", size=(20, 1), font=FONT+str(16)), sg.Button("Exit", size=(20, 1), font=FONT+str(16))]
    ]

    # Window initialization
    window = sg.Window("CS50P Project", layout, element_justification="c", finalize=True)

    # Bind Enter key to search button
    window["Input1"].bind("<Return>", "_Enter")

    # Event loop
    while True:
        event, values = window.read()
        # If app is closed without the user entering a value
        try:
            user_input = values["Input1"].strip()
        except TypeError:
            break

        if event == sg.WIN_CLOSED or event == "Exit":
            print("Exiting application.")
            break

        if event == "Search" or event == "Input1" + "_Enter":
            # Pop up window when user does not enter a value
            if not user_input:
                no_input_popup()
            else:
                print("Your input was: ", user_input)


    window.close()

def no_input_popup():
    sg.popup("Error", "Please enter a valid input in the search bar.", font=FONT+str(18))


if __name__ == "__main__":
    main()
