# Methods to display menu windows in GUI
import webbrowser
from tkinter import *
from actions import *
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Menu for udpating credentials
def credentialsMenu():
    cred = c.execute("SELECT * FROM credentials")
    creds = cred.fetchall()
    if creds:
        print(creds)
        openWeatherAppID = creds[0][0]
        weatherAPIKey = creds[0][1]
        weatherBitKey = creds[0][2]
    else:
        openWeatherAppID = ""
        weatherAPIKey = ""
        weatherBitKey = ""  
    credentialWindow = Toplevel()
    credentialWindow.iconbitmap('credential.ico')
    openWeatherLabel = Label(credentialWindow, text="Open Weather AppID:")
    openWeatherEntry = Entry(credentialWindow, width=50)
    openWeatherEntry.insert(END, openWeatherAppID)
    weatherAPILabel = Label(credentialWindow, text="Weather API Key:")
    weatherAPIEntry = Entry(credentialWindow, width=50)
    weatherAPIEntry.insert(END, weatherAPIKey)
    weatherBitLabel = Label(credentialWindow, text="Weatherbit API Key:")
    weatherBitEntry = Entry(credentialWindow, width=50)
    weatherBitEntry.insert(END, weatherBitKey)
    submitButton = ttk.Button(credentialWindow, text="Update Credentials:", command = lambda: updateCredentials(openWeatherEntry.get(), weatherAPIEntry.get(), weatherBitEntry.get(), credentialWindow, openWeatherAppID, weatherAPIKey, weatherBitKey))
    openWeatherLabel.grid(row=1, column=1)
    openWeatherEntry.grid(row=1, column=2)
    weatherAPILabel.grid(row=2, column=1)
    weatherAPIEntry.grid(row=2, column=2)
    weatherBitLabel.grid(row=3, column=1)
    weatherBitEntry.grid(row=3, column=2)
    submitButton.grid(row=4, column=2)

# Menu for adding locations to the database
def addLocationMenu():
    addLocationWindow = Toplevel()
    addLocationWindow.iconbitmap('mountain.ico')
    nameLabel = Label(addLocationWindow, text="Location Name:")
    nameEntry = Entry(addLocationWindow, width=50)
    lattitudeLabel = Label(addLocationWindow, text="Location Lattitude:")
    lattitudeEntry = Entry(addLocationWindow, width=50)
    longitudeLabel = Label(addLocationWindow, text="Location Longitude:")
    longitudeEntry = Entry(addLocationWindow, width=50)
    submitButton = ttk.Button(addLocationWindow, text="Add Location", command=lambda: addLocation(nameEntry.get(), lattitudeEntry.get(), longitudeEntry.get(), addLocationWindow))
    nameLabel.grid(row=1, column=1)
    nameEntry.grid(row=1, column=2)
    lattitudeLabel.grid(row=2, column=1)
    lattitudeEntry.grid(row=2, column=2)
    longitudeLabel.grid(row=3, column=1)
    longitudeEntry.grid(row=3, column=2)
    submitButton.grid(row=4, column=2)

# Menu for removing locations from the database
def removeLocationMenu():
    removeLocationWindow = Toplevel()
    removeLocationWindow.iconbitmap('mountain.ico')
    nameLabel = Label(removeLocationWindow, text="Location Name:")
    nameEntry = Entry(removeLocationWindow, width=50)
    submitButton = ttk.Button(removeLocationWindow, text="Remove Location", command=lambda: removeLocation(nameEntry.get(), removeLocationWindow))
    nameLabel.grid(row=1, column=1)
    nameEntry.grid(row=1, column=2)
    submitButton.grid(row=2, column=2)

# Help window    
def helpMenu():
    def callback(url):
        webbrowser.open_new_tab(url)
        
    helpWindow = Toplevel()
    helpWindow.iconbitmap('question.ico')
    helpLabel = Label(helpWindow, text="Powderbot GUI")
    helpLabel1 = Label(helpWindow, text="Powderbot gathers snowfall forecast information from three weather APIs by GPS coordinates.\n In order for the program to work you need to register for a free API key from each of the APIs.")
    helpLabel2 = Label(helpWindow, text="Open Weather", fg="blue", cursor="hand2")
    helpLabel2.bind("<Button-1>", lambda e: callback("https://home.openweathermap.org/users/sign_up"))
    helpLabel3 = Label(helpWindow, text="Weather API", fg="blue", cursor="hand2")
    helpLabel3.bind("<Button-1>", lambda e: callback("https://www.weatherapi.com/signup.aspx"))
    helpLabel4 = Label(helpWindow, text="Weatherbit I/O", fg="blue", cursor="hand2")
    helpLabel4.bind("<Button-1>", lambda e: callback("https://www.weatherbit.io/account/create"))
    helpLabel5 = Label(helpWindow, text = "Enter the corresponding values in the Update Credentials menu.")
    helpLabel6 = Label(helpWindow, text="Use Add Locations menu to add locations, entering lattitude and longitude in decimal form. EX: lat = 38.40889, lon = -79.99472")
    helpLabel7 = Label(helpWindow, text="Remove locations by entering the name of the location in the form in the Remove Locations menu.\nIf not working properly, check that all credentials and location coordinates are valid and in the correct format.")
    helpLabel8 = Label(helpWindow, text="If you are only looking for resort locaitons in the US you can use the Powderbot Online.")
    helpLabel9 = Label(helpWindow, text="Powderbot Online.", fg = "blue", cursor="hand2")
    helpLabel9.bind("<Button-1>", lambda e: callback("https://powderbot.pythonanywhere.com/"))
    helpLabel10 = Label(helpWindow, text="Register to save 4 favorites and enable search/filtering by Pass, State, or Reigon")
    helpLabel.grid(row=1, column=2)
    helpLabel1.grid(row=2, column=2)
    helpLabel2.grid(row=3, column=1)
    helpLabel3.grid(row=3, column=2)
    helpLabel4.grid(row=3, column=3)
    helpLabel5.grid(row=4, column=2)
    helpLabel6.grid(row=5, column=2)
    helpLabel7.grid(row=6, column=2)
    helpLabel8.grid(row=7, column=2)
    helpLabel9.grid(row=8, column=2)
    helpLabel10.grid(row=9, column=2)
