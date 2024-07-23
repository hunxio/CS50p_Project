
<div align="center"> <h1>CS50P WEATHER PROJECT</h1> </div>

<div align="center">
	<img src="logo.png">
</div>

<div align="center"><h3>Video Demo:</h3></div>  
<div align="center"><p>TBD</p></div>  

### Introduction:
Hello everyone, my name is Hunxio, and here you will find a brief explanation about my Final Project for CS50P ! This Final Project is made using Python and various tools we have learnt and used through the course, like libraries, APIs and many more. The code has comments and type hints to give a better reading and understing of the functions and what they do. I have tried to make a GUI to make this program easier to try out and/or test for everyone, a separate version of this program executable can be accessible to everyone requesting me here on my [GitHub](https://github.com/hunxio/CS50p_Project).
### Description:

You will find in the root folder 5 files, here is what they do:
- **.gitignore** : it does not upload on GitHub when you commit some changes to your code, the files specified in file. Sensible or private date should always be saved somewhere else and not shown in public accessible files;
- **logo.png** : this is the image logo i have used for my program icon and logo;
- **project.py** : this is the main *.py* file where the program's code is stored, it contains several functions (their utility explained later on) and I tried to include as many notions we learnt during the CS50P course;
- **requirements.txt** : you will find here all the libraries and packages needed to execute and run this program, if you are working on multiple devices on your projects it is really nice to keep track of all the libraries you need without having to install them all one by one everytime. They can all be installed by using the followin command: 
    
  `pip install -r requirements.txt`
  
 -  **test_project.py** : used with pytest to test out functions and check their results. Because most, if not all, of my functions give back always different results depending on when they are called (APIs for geolocalization, or API weather) unit testing this program has been quite tedious.

Here down below you will find an explanation of project.py and how it works:

 At the top you can find all the libraries needed, we are importing them (some times we only import some objects of them, in other cases we import the complete library);
 - **main** : it is really small and it only calls for one function which then calls for other ones, we define a window, call for app_gui() function and then window.mainloop(). This defines the window for the GUI and we keep it always running with window.mainloop(), so it does not close as long as we do not want to close it;
 - **app_gui()** : most of the informations about the window, its widgets and else is stored here, you will find snippets of code for their size, color, content, text etc. There are also global variables which will be used later on in other functions which will modify directly the variables in app_gui();
 - **validation()**: once you click on the "serch button in the UI", this function will do some checks on the user input: first it will check if the user actually prompted for an input, if the user did insert an input it will check if that input is valid or not. In case the input is invalid or the user did not enter any input, it will return back an error. In case everything was fine, get_coordinates() will be called, returning us back the latitude and longitude in a dictionary for the location desired; this informations will be needed to retrieve data from our weather api (in particular the temperature in Celsius, humidity% and precipation%);
 - **temperature_api()**: this functions require two arguments to work: latitde and longitude which are both going to be float values. It will send out a request and retrieve back data which will be later on "unpacked" and returned as a dictionary. Thanks to [Open-Meteo.com](https://open-meteo.com/) for the API service;
 - **get_coordinates()**: it requires one argument, which is the name of a location. This will call for a service to return us back the latitude and longitude of the desired place (of course they might change because of the size of cities). You can find more about it [here](https://pypi.org/project/geopy/), by consulting their documentation;
 - **window_update()**: it requires three arguments, they will be used to make some widgets in the GUI visible, the arguments will be inserted in the text field of the widget and displayed to the user;
 - **update_weather()**: last but not least, this function will check if the return value from *validation()* is a dictionary or else. Because of how validation() it is built, it will either return a dictionary or a string, depending if it encountered an error or not. In the first case, where it returns a dictionary, it will "hide" (more like remove) an eventually present error text and show the values for the temperature, humidity and precipitation. In the other case, it will "hide" the informations about the temperature, humidity and precipitation (if they exist) and show a message error which can vary depending on the origin of the issue.

As good practice explained during the CS50P course, we find 

    if __name__ == "__main__":
        main()

This will prevent the program to run the main function unless we call the main function to be executed.

### Resources:

[Open-Meteo](open-meteo.com) - for providing a free non-commercial use API

### Contacts:
[Hunxio's GitHub](https://github.com/hunxio)

  
  
