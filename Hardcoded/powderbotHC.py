#########################################################################################################################
# This program when ran gathers snowfall amount forecast information for a location you choose and averages it for output
#Forecast information provided by 
  #Open Weather  https://home.openweathermap.org/users/sign_up
  #Weather API   https://www.weatherapi.com/signup.aspx
  #Weatherbit    https://www.weatherbit.io/account/create
#########################################################################################################################

import requests
import time
import tweepy

# Enter your credentials in the appropriate variable between the ""
locationName = "" # Enter the name of your mountain to add at end of forecast for twitter.  Leave blank if desired.
lattitude = "" # Enter the lattitude of the location you want the forecast for in decimal form
longitude = "" # Enter the longitude of the location you want the forecast for in decimal form
openWeatherAppID = "" # Enter your openweather App ID
weatherAPIKey = "" # Enter your weatherapi.com API Key
weatherBitKey = "" # Enter your weatherbit.io API Key
twitterConsumerKey = "" # Enter your Twitter consumer key
twitterConsumerSeceret = "" # Enter your Twitter consumer seceret
twitterAccessToken = "" # Enter your Twitter access token
twitterAccessTokenSeceret = "" # Enter your Twitter access token seceret

aggregateSnowfall = {} # Holds aggregate snowfall for each day while getting forecast
aggregateForecast = {} # Holds aggregate forecast form each call
tweet = "" # Holds the forecast to be given

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
            forecastDays[date] = ["snow", day["weather"][0]["description"], (day["snow"]/2.54)] # /2.54 because amounts are given in cm
      
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
        forecastDays[date] = [entry["day"]["condition"]["text"], entry["day"]["condition"]["code"], entry["day"]["daily_will_it_snow"], entry["day"]["totalprecip_in"]]
    
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
        forecastDays[date] = (day["weather"]["description"], day["snow_depth"], day["snow"])

    return forecastDays # Returns dictonary of forecast by days

# Compiles and averages snowfall forecast information from each weather service
def compileSnowfall(openWeather, weatherAPI, weatherBit, aggregateSnowfall):
    # Process info from weatherbit call into aggregate snowfall
    for day in weatherBit:
        aggregateSnowfall[day] = [weatherBit[day][2]]
    # Process info from weatherAPI call into aggregate snowfall
    for day in weatherAPI:
        aggregateSnowfall[day].append(weatherAPI[day][3])
    # Process info from open weather call into aggregate snowfall
    for day in openWeather:
        if openWeather[day][0] == "snow":
            aggregateSnowfall[day].append(openWeather[day][2])
    # Averages snowfall forecasts for each day
    for day in aggregateSnowfall:
      aggregateSnowfall[day] = "{:.2f}".format(sum(aggregateSnowfall[day])/len(aggregateSnowfall[day]))

# Generates the output for terminal or twitter
def composeTweet (aggregateSnowfall, tweet, locationName):
    # For each day change the output for the amount of snow.  6" rule
    for day, snowfall in aggregateSnowfall.items():
        if float(snowfall) > 3 and float(snowfall) < 6:
            tweet += "{} {}in \u2744😎\u2744\n\n".format(day, snowfall) 
        elif float(snowfall) >= 6:
            tweet += "{} {}in \u2744\u2744POWDER!\u2744\u2744\n\n".format(day, snowfall)
        elif float(snowfall) > 0:
            tweet += "{} {}in \u2744\n\n".format(day, snowfall)
        else:
            tweet += "{} No Snow ☹️\n\n".format(day)

    tweet += ("#" + locationName) # Adds location name to output 
    return tweet

# Posts the forecast to twitter
def postToTwitter(twitterConsumerKey, twitterConsumerSeceret, twitterAccessToken, twitterAccessTokenSeceret, tweet):
   # Twitter access
    auth = tweepy.OAuthHandler(twitterConsumerKey, twitterConsumerSeceret)
    auth.set_access_token(twitterAccessToken, twitterAccessTokenSeceret)
    # Create API object
    twitter = tweepy.API(auth)   
    # Post a tweet:
    try:
        twitter.update_status(tweet)    
    except:
        print("Error Posting") # Occurs if it is a duplicate tweet within a certain time frame

    return null    

# Makes calls to each weather service
# Gets snowfall forecast for open weather
openWeather = openWeatherCall(lattitude, longitude, openWeatherAppID) 
# Gets snowfall forecast for weatherAPI
weatherAPI = weatherAPICall(lattitude, longitude, weatherAPIKey)
# Gets snowfall forecast for weatherbit
weatherBit = weatherBitCall(lattitude, longitude, weatherBitKey)
# Averages snowfall from sources
compileSnowfall(openWeather, weatherAPI, weatherBit, aggregateSnowfall)
# Creates the output
tweet = composeTweet (aggregateSnowfall, tweet, locationName)
 # Outputs results/tweet to terminal
print(tweet)
# Post the output to twitter.  Comment this line out if you don't want to post to twitter.
postToTwitter(twitterConsumerKey, twitterConsumerSeceret, twitterAccessToken, twitterAccessTokenSeceret, tweet)







