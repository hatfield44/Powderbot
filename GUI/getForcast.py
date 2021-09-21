# Methods to retrieve forecast information from APIs and store in database
import requests
import time
from datetime import datetime
import sqlite3

# Retrieves forecast data from APIs and store in the database
# @param openWeatherAppID   Openweather API key
# @param weatherAPIKey      weatherAPI API key
# @param weatherBitKey      weatherBit API key
def getForecast(openWeatherAppID, weatherAPIKey, weatherBitKey):
    print("\nGetting Forecast\n")

    # connect to the databas
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

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
        weatherAPIcomURL = "http://api.weatherapi.com/v1/forecast.json?key=" + weatherAPIKey + "&q=" + lattitude + "," + longitude + "&days=10"
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
        weatherBitURL = "https://api.weatherbit.io/v2.0/forecast/daily?lat="+ lattitude + "&lon=" + longitude + "&days=10&units=I&key=" + weatherBitKey
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

    # Aggregates snowfall forecasts and averages them, returning the averages for each date in a dictonary
    def forecastAggregation(lattitude, longitude):
        aggregateSnowfall = {} # Holds aggregate snowfall for each day while getting forecast
        aggregateForecast = {} # Holds aggregate forecast form each call
        # Get forecast for location from each API
        openWeather = openWeatherCall(lattitude, longitude, openWeatherAppID)
        weatherAPI = weatherAPICall(lattitude, longitude, weatherAPIKey)
        weatherBit = weatherBitCall(lattitude, longitude, weatherBitKey)
        # Order forecast amounts by date from each API
        for date, forecast in weatherBit.items():
            aggregateSnowfall[date] = [forecast]

        for date, forecast in weatherAPI.items():
            aggregateSnowfall[date].append(forecast)

        for date, forecast in openWeather.items():
                aggregateSnowfall[date].append(forecast)

        for date, prediction in aggregateSnowfall.items():
            aggregateForecast[date] = "{:.2f}".format(sum(aggregateSnowfall[date])/len(aggregateSnowfall[date]))
        return aggregateForecast

    # Retrieves the forecast and aggregates it for each location and stores it in the database
    def dbForecast():
        # Get list of locations
        locations = c.execute("SELECT * FROM locations").fetchall()
        # For each location in the database retrieve the forecast and store it in database
        for location in locations:
            for row in c.execute("SELECT lat FROM locations WHERE name =" + "'"+location[0]+"'"):
                lattitude = str(row).replace("',)", "")
                lattitude = lattitude.replace("('", "")
            for row in c.execute("SELECT lon FROM locations WHERE name =" + "'"+location[0]+"'"):
                longitutde = str(row).replace("',)", "")
                longitutde = longitutde.replace ("('", "")
            # get forecast info
            forecast = forecastAggregation(lattitude, longitutde)
            output = []
            for date, amount in forecast.items():
                output.append(amount)
            name = str(location[0])
            # store in db 
            for j in range(0, 10):
                column = "forecast" + str(j)
                c.execute("UPDATE locations SET " + column + "= " + output[j] + " WHERE name =" + "'"+location[0]+"'")

            conn.commit()

    dbForecast()
    conn.close()
    print("Forecast Retrieved : " + str(datetime.now()))



