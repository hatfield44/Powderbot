import requests
import time
from datetime import datetime
from config import openWeatherAppID, weatherAPIKey, weatherBitKey
import sqlite3

def test():
    print('test')

def getForecast():
    print("\nGetting Forecast\n")

    conn = sqlite3.connect('website/database.db')
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
        weatherAPIcomURL = "http://api.weatherapi.com/v1/forecast.json?key=8f62acbc4d494321a97221253200811&q=" + lattitude + "," + longitude + "&days=10"
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

    def forecastAggregation(lattitude, longitude):
        aggregateSnowfall = {} # Holds aggregate snowfall for each day while getting forecast
        aggregateForecast = {} # Holds aggregate forecast form each call

        openWeather = openWeatherCall(lattitude, longitude, openWeatherAppID)
        weatherAPI = weatherAPICall(lattitude, longitude, weatherAPIKey)
        weatherBit = weatherBitCall(lattitude, longitude, weatherBitKey)

        for date, forecast in weatherBit.items():
            aggregateSnowfall[date] = [forecast]

        for date, forecast in weatherAPI.items():
            aggregateSnowfall[date].append(forecast)

        for date, forecast in openWeather.items():
                aggregateSnowfall[date].append(forecast)

        for date, prediction in aggregateSnowfall.items():
            aggregateForecast[date] = "{:.2f}".format(sum(aggregateSnowfall[date])/len(aggregateSnowfall[date]))
        return aggregateForecast


    def dbForecast():
        for i in range(1, 330):
            for row in c.execute("SELECT lat FROM location WHERE id =" + str(i)):
                lattitude = str(row).replace("',)", "")
                lattitude = lattitude.replace("('", "")
            for row in c.execute("SELECT lon FROM location WHERE id =" + str(i)):
                longitutde = str(row).replace("',)", "")
                longitutde = longitutde.replace ("('", "")
            # get forecast info
            forecast = forecastAggregation(lattitude, longitutde)
            output = []
            for date, amount in forecast.items():
                output.append(amount)
            print(output)
            # store in db 
            for j in range(0, 10):
                column = "forecast" + str(j)
                c.execute("UPDATE location SET " + column + "= " + output[j] + " WHERE id =" + str(i))

            conn.commit()

    dbForecast()
    conn.close()
    print("Forecast Retrieved : " + str(datetime.now()))


getForecast()
