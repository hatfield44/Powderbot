# Methods to perform actions in the database
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from getForecast import getForecast
from getDates import getDates
from getForecast import getForecast

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Method to update user API keys
def updateCredentials(openWeather, weatherAPI, weatherBit, credentialWindow, openWeatherAppID, weatherAPIKey, weatherBitKey):
    if openWeatherAppID == "" and weatherAPIKey == "" and weatherBitKey == "":
        openWeatherAppID = openWeather
        weatherAPIKey = weatherAPI
        weatherBitKey = weatherBit
        c.execute("INSERT INTO credentials VALUES("+"'"+openWeatherAppID+"'"+", "+"'"+weatherAPIKey+"'"+", "+ "'"+weatherBitKey+"'"")")
    else:
        openWeatherAppID = openWeather
        weatherAPIKey = weatherAPI
        weatherBitKey = weatherBit
        c.execute("UPDATE credentials SET openWeather =" + "'"+ openWeatherAppID +"'"+", weatherAPI ="+"'"+ weatherAPIKey +"'"+ ", weatherBit ="+ "'"+weatherBitKey+"'" )
    messagebox.showinfo("SUCESS", "  Credentials Updated!\n Please restart program.")
    conn.commit()
    credentialWindow.destroy()

# Action to add Location to database
def addLocation(name, lattitude, longitude, addLocationWindow):
    c.execute("INSERT INTO locations VALUES("+"'"+name+"'"+", "+lattitude+", "+ longitude+", 0,0,0,0,0,0,0,0,0,0)")
    conn.commit()
    messagebox.showinfo("SUCESS", "Location added to locations!")
    addLocationWindow.destroy()

# Action to remove Location from database
def removeLocation(name, removeLocationWindow):
    exists = FALSE
    for location in c.execute("SELECT * FROM locations WHERE name = '"+name+"'").fetchall():
        if (name in location):
            exists = TRUE
    if exists == TRUE:
        c.execute("DELETE FROM locations WHERE name = '"+name+"'")
        conn.commit()
        messagebox.showinfo("SUCESS", "Location removed from locations")
        removeLocationWindow.destroy()
    else:
         messagebox.showinfo("ERROR", "Name not found in locations!")

# Action to update forecast information in database and display forecasts
def forecastUpdate(openWeatherAppID, weatherAPIKey, weatherBitKey):
    getForecast(openWeatherAppID, weatherAPIKey, weatherBitKey)
    forecast = Toplevel()
    forecast.iconbitmap('snowflake.ico')
    forecast.geometry("-0+65")
    tree = ttk.Treeview(forecast)
    dates = getDates()
    # Create a tree to display the forecasts information    
    tree['columns'] = ('Name', 'Forecast1', 'Forecast2', 'Forecast3', 'Forecast4', 'Forecast5', 'Forecast6', 'Forecast7', 'Forecast8', 'Forecast9', 'Forecast10',)
    tree.column('#0', width = 0, stretch=NO)
    tree.column('Name', anchor=CENTER, width=200)
    tree.column('Forecast1', anchor=CENTER, width=80)
    tree.column('Forecast2', anchor=CENTER, width=80)
    tree.column('Forecast3', anchor=CENTER, width=80)
    tree.column('Forecast4', anchor=CENTER, width=80)
    tree.column('Forecast5', anchor=CENTER, width=80)
    tree.column('Forecast6', anchor=CENTER, width=80)
    tree.column('Forecast7', anchor=CENTER, width=80)
    tree.column('Forecast8', anchor=CENTER, width=80)
    tree.column('Forecast9', anchor=CENTER, width=80)
    tree.column('Forecast10', anchor=CENTER, width=80)
    tree.heading('Name', text='Name')
    tree.heading('Forecast1', text =  dates[0])
    tree.heading('Forecast2', text = dates[1])
    tree.heading('Forecast3', text = dates[2])
    tree.heading('Forecast4', text = dates[3])
    tree.heading('Forecast5', text = dates[4])
    tree.heading('Forecast6', text = dates[5])
    tree.heading('Forecast7', text = dates[6])
    tree.heading('Forecast8', text = dates[7])
    tree.heading('Forecast9', text = dates[8])
    tree.heading('Forecast10', text = dates[9])

    # Add the name and forecast from each location in database to the tree
    for location in c.execute("SELECT * FROM locations").fetchall():
        i = 2
        print(location)
        tree.insert(parent='', index=i, text='', values=(location[0], location[3], location[4], location[5], location[6], location[7], location[8], location[9], location[10], location[11], location[12]))
        i += 1
    tree.pack()
    return forecast
