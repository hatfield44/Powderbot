#!/usr/bin/python3.8

import requests
import time
from datetime import datetime
from config import openWeatherAppID, weatherAPIKey, weatherBitKey, visualCrossingKey
import sqlite3

def test():
    print('test')

def getForecast():
    print("\nGetting Forecast\n")

    conn = sqlite3.connect('/database.db')
    c = conn.cursor()

    # Gets forecast from Visual Crossing
    def visualCrossingCall(lattitude, longitude, visualCrossingKey):
        # Creates URL for call
        url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?locations=" + lattitude + "," + longitude + "&aggregateHours=24&unitGroup=us&shortColumnNames=false&contentType=json&key=" + visualCrossingKey
        data = requests.get(url) # Performs call and gets data
        forecast = data.json() # Process data to JSON
        forecastDays = {} # Dictionary to hold each days forecast

        # For each day of the forecast add the date and snowfall amount to forecastDays
        for day in forecast["locations"][lattitude + "," + longitude]["values"]:
            longDate = day["datetimeStr"] # Gets date and time
            splitdate = longDate.split("T") # Splits date and time
            date = splitdate[0]
            date = date[5:7] + "/" + date[8:] + "/" + date[2:4] # Formats date
            # deals with the last date being "none" instead of a number
            if type(day["snow"]) == float:
                forecastDays[date] = day["snow"]

        return forecastDays # Returns dictonary of forecast by days

    # Gets forecast from Open Weather
    def openWeatherCall(lattitude, longitude, openWeatherAppID):
        # Creates URL for call
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + lattitude + "&lon=" + longitude + "&exclude=current,minutely,hourly&units=standard&appid=" + openWeatherAppID
        data = requests.get(url) # Performs call and gets data
        forecast = data.json() # Process dtat to JSON
        forecastDays = {} # Dictionary to hold each days forecast

        # For each day in the forecast; if it has snow add it to forecastDays
        for day in forecast["daily"]:
            date = time.strftime("%x", time.localtime(day["dt"])) # Process the date from JSON
            if "snow" in day:
                forecastDays[date] = (day["snow"]/2.54)
            else:
                forecastDays[date] = 0

        return forecastDays # Returns dictonary of forecast by days


    # Gets forecast from weather API
    def weatherAPICall(lattitude, longitude, weatherAPIKey):
        # URL for the API call
        weatherAPIcomURL = "http://api.weatherapi.com/v1/forecast.json?key=8f62acbc4d494321a97221253200811&days=3&q=" + lattitude + "," + longitude
        data = requests.post(weatherAPIcomURL) # Requests the data
        forecastData = data.json() # Processes data in JSON format
        forecastDays = {} # Dictonary to hold forecast to return data to main program

        # Loops through forecast data adding the relevant info to the forecastDays dictonary
        for entry in forecastData["forecast"]["forecastday"]:
            #Gets date
            LongDate = entry["date"]
            date = LongDate[5:7], "/", LongDate[8:10], "/", LongDate[2:4]
            date = "".join(date)
            if entry["day"]["daily_will_it_snow"] == 1:
                forecastDays[date] = entry["day"]["totalprecip_in"]
            else:
                forecastDays[date] = 0

        return forecastDays # Returns dictonary of forecast by days


    # Gets forecast from weather bit
    def weatherBitCall(lattitude, longitude, weatherBitKey):
        weatherBitURL = "https://api.weatherbit.io/v2.0/forecast/daily?lat="+ lattitude + "&lon=" + longitude + "&days=15&units=I&key=" + weatherBitKey
        data = requests.post(weatherBitURL) # Requests the data
        forecast = data.json() # Processes data in JSON format
        forecastDays = {} # Dictonary to hold forecast to return data to main program

        # Loops through forecast data adding the relevant info to the forecastDays dictonary
        for day in forecast["data"]:
            # Gets date
            LongDate = day["valid_date"]
            date = LongDate[5:7], "/", LongDate[8:10], "/", LongDate[2:4]
            date = "".join(date)
            forecastDays[date] = day["snow"]

        return forecastDays # Returns dictonary of forecast by days

    def forecastAggregation(lattitude, longitude):
        aggregateSnowfall = {} # Holds aggregate snowfall for each day while getting forecast
        aggregateForecast = {} # Holds aggregate forecast form each call
        retrievedDays = 0 # Holds number of forecast days retrieved in case an API doesn't respond

        # Try calling Visual Crossing and print error message if problem arises otherwise add days forecast to aggregateSnowfall
        try:
            visualCrossing = visualCrossingCall(lattitude, longitude, visualCrossingKey)
        except:
            print("visualCrossing Error")
        else:
            for date, forecast in visualCrossing.items():
                aggregateSnowfall[date] = [forecast]
                retrievedDays = 15

        # Try calling WeatherBit and print error message if problem arises otherwise add days forecast to aggregateSnowfall
        try:
            weatherBit = weatherBitCall(lattitude, longitude, weatherBitKey)
        except:
            print("WeatherBit Error")
        else:
            for date, forecast in weatherBit.items():
                try:
                    aggregateSnowfall[date].append([forecast])
                except:
                    aggregateSnowfall[date] = [forecast]
                    retrievedDays = 10

        # Try calling OpenWeather and print error message if problem arises otherwise add days forecast to aggregateSnowfall
        try:
            openWeather = openWeatherCall(lattitude, longitude, openWeatherAppID)
        except:
            print("OpenWeather Error")
        else:
            for date, forecast in openWeather.items():
                try:
                    aggregateSnowfall[date].append(forecast)
                except:
                    aggregateSnowfall[date] = [forecast]
                    retrievedDays = 8

        # Try calling WeatherAPI and print error message if problem arises otherwise add days forecast to aggregateSnowfall
        try:
            weatherAPI = weatherAPICall(lattitude, longitude, weatherAPIKey)
        except:
            print("Weather API Error")
        else:
            for date, forecast in weatherAPI.items():
                try:
                    aggregateSnowfall[date].append(forecast)
                except:
                    aggregateSnowfall[date] = [forecast]
                    retrievedDays = 3

        # Gets the average from the snowfall totals for each date
        for date, prediction in aggregateSnowfall.items():
            aggregateForecast[date] = "{:.2f}".format(sum(aggregateSnowfall[date])/len(aggregateSnowfall[date]))
        aggregateForecast["days"] = retrievedDays

        return aggregateForecast


    def dbForecast():
        c.execute("SELECT COUNT(*) FROM location")  # Gets number of locations from DB
        mountainCount = c.fetchone()[0]  # Variable used to hold number of locations
        for i in range(1, mountainCount + 1):
            for row in c.execute("SELECT name FROM location WHERE id =" + str(i)):
                print(str(row)[2:-3])
            for row in c.execute("SELECT lat FROM location WHERE id =" + str(i)):
                lattitude = str(row).replace("',)", "")
                lattitude = lattitude.replace("('", "")
            for row in c.execute("SELECT lon FROM location WHERE id =" + str(i)):
                longitude = str(row).replace("',)", "")
                longitude = longitude.replace ("('", "")
            # get forecast info
            forecast = forecastAggregation(lattitude, longitude)
            output = []
            for date, amount in forecast.items():
                output.append(amount)
            print(output)
            # store in db
            for j in range(0, forecast["days"]):
                column = "forecast" + str(j)
                c.execute("UPDATE location SET " + column + "= " + output[j] + " WHERE id =" + str(i))

            conn.commit()

    dbForecast()
    conn.close()
    print("Forecast Retrieved : " + str(datetime.now()))


getForecast()
