# Program that allows a user to add/check locations for snowfall forecast by lat/lon
from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import date
from actions import *
from menus import *

if __name__ == "__main__":
    # Create/Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create Table if it does not exist
    c.execute("CREATE TABLE IF NOT EXISTS locations (name VARCHAR(50) NOT NULL, lat VARCHAR(50) NOT NULL, lon VARCHAR(50) NOT NULL, forecast0 VARCHAR(50) NOT NULL, forecast1 VARCHAR(50) NOT NULL, forecast2 VARCHAR(50) NOT NULL, forecast3 VARCHAR(50) NOT NULL, forecast4 VARCHAR(50) NOT NULL, forecast5 VARCHAR(50) NOT NULL, forecast6 VARCHAR(50) NOT NULL, forecast7 VARCHAR(50) NOT NULL, forecast8 VARCHAR(50) NOT NULL, forecast9 VARCHAR(50) NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS credentials (openWeather VARCHAR(50) NOT NULL, weatherAPI VARCHAR(50) NOT NULL, weatherBit VARCHAR(50) NOT NULL)")
    conn.commit()

    # Check for credentials already existing
    # If they exist set the variables to the corresponding credentials
    # else set the variables to an empty string
    cred = c.execute("SELECT * FROM credentials")
    creds = cred.fetchall()
    if creds:
        openWeatherAppID = creds[0][0]
        weatherAPIKey = creds[0][1]
        weatherBitKey = creds[0][2]
    else:
        openWeatherAppID = ""
        weatherAPIKey = ""
        weatherBitKey = ""

    # Create the root window
    root = Tk()
    root.iconbitmap('logo.ico')
    root.geometry("550x30-0+0")
    # If the user has already entered credentials, retrieve the forecast upon opening program
    # else show the user a message to enter their credentials
    if openWeatherAppID != "" and weatherAPIKey != "" and weatherBitKey != "":
        forecast = forecastUpdate(openWeatherAppID, weatherAPIKey, weatherBitKey)
    else: 
        messagebox.showwarning("Warning", "Please update credentials!")
        # Creates instance of Toplevel to be destroyed when Update Forecast Button clicked
        forecast = Toplevel()
        forecast.withdraw()
    credentialsButton = ttk.Button(root, text="Update Credentials", command= lambda: credentialsMenu())
    addLocationButton = ttk.Button(root, text = "Add Location", command=addLocationMenu)
    removeLocationButton = ttk.Button(root, text = "Remove Location", command=removeLocationMenu)
    helpButton = ttk.Button(root, text = "Help", command=helpMenu)
    updateButton = ttk.Button(root, text = "Update Forecast", command=lambda: [forecast.destroy(), forecastUpdate(openWeatherAppID, weatherAPIKey, weatherBitKey)])
    credentialsButton.grid(row=0, column=1)
    addLocationButton.grid(row=0, column=2)
    removeLocationButton.grid(row=0, column=3)
    updateButton.grid(row=0, column = 4)
    helpButton.grid(row=0, column=5)


    root.mainloop()

