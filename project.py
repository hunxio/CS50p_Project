import PySimpleGUI as sg


def main():
    # Elements inside the window
    layout = [
        [sg.Text("Test field for input:")],
        [sg.Input("", key="Input1")],
        [sg.Button("Search"), sg.Button("Exit")],
    ]
    # Window initialization
    window = sg.Window("CS50P Project", layout, finalize=True)
    window["Input1"].bind("<Return>", "_Enter")
    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "Search" or event == "Input1" + "_Enter":
            print("output:", values["Input1"])

    window.close()


if __name__ == "__main__":
    main()
