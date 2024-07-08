import PySimpleGUI as sg


def main():
    # Elements inside the window
    layout = [
        [sg.Text("Welcome to my CS50P Project!")],
        [sg.Text("User input field:"), sg.Input("", key="Input1")],
        [sg.Button("Search"), sg.Button("Exit")]
    ]

    # Window initialization
    window = sg.Window("CS50P Project", layout, finalize=True)

    # Bind Enter key to search button
    window["Input1"].bind("<Return>", "_Enter")

    # Event loop
    while True:
        event, values = window.read()
        user_input = values["Input1"].strip()
        if event == sg.WIN_CLOSED or event == "Exit":
            print("Exiting Applicaiton...")
            break

        if event == "Search" or event == "Input1" + "_Enter":
            if user_input == "" or user_input is None:
                    layout = [[sg.Text("Something went wrong during the process...")], [sg.Text("Please enter a value in the search bar.")], [sg.Button("Exit")]]
                    error_window = sg.Window("Error", layout, finalize=True)
                    while True:
                        event, _ = error_window.read()
                        if event == sg.WIN_CLOSED or event == "Exit":
                            break
            else:
                print("Your input was: ", user_input)
                break


    window.close()


if __name__ == "__main__":
    main()
