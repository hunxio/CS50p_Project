import PySimpleGUI as sg


def main():
    # Elements inside the window
    layout = [
        [sg.Text("Welcome to my CS50P Project!", size=(25, 1), font="Arial")],
        [sg.Text("User input field:", size=(11, 1), font="Arial"), sg.Input("", key="Input1")],
        [sg.Button("Search", size=(22, 1), font="Arial"), sg.Button("Exit", size=(22, 1), font="Arial")]
    ]

    # Window initialization
    window = sg.Window("CS50P Project", layout, finalize=True, element_justification="c")

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
            print("Exiting Applicaiton.")
            break

        if event == "Search" or event == "Input1" + "_Enter":
            # Pop up window when user does not enter a value
            if user_input == "" or user_input is None:
                    layout = [[sg.Text("Something went wrong during the process...", size=(30, 1), font="Arial")], 
                    [sg.Text("Please enter a value in the search bar.", size=(30, 1), font="Arial")], 
                    [sg.Button("Close", size=(20, 1), font="Arial")]]
                    error_window = sg.Window("Error", layout, finalize=True, element_justification="c")
                    while True:
                        event, _ = error_window.read()
                        if event == sg.WIN_CLOSED or event == "Close":
                            break
            else:
                print("Your input was: ", user_input)
                break


    window.close()


if __name__ == "__main__":
    main()
