**Powderbot**

Various implementations of an app to aid in powder chasing by providing snowfall forecasts for the current day and next 9 days by lattitude and longitude.

Forecast information provided by:

  Open Weather  https://home.openweathermap.org/users/sign_up
  
  Weather API   https://www.weatherapi.com/signup.aspx
  
  Weatherbit    https://www.weatherbit.io/account/create

- Hardcoded version requires the user to enter their credentials and location information directly into the code.
  - Only retrieves the forecast for one location and outputs the forecast as a tweet
  - Prints forecast/tweet to the terminal

- CLI version allows the user to enter their credentials and location info on the inital run of the program and stores them in a text file.
  - If the forecast for more than one location is being retrieved the user should choose not to post to twitter as the tweet will grow to large to post.
  - Prints the forecast/tweet to the terminal
  
- GUI version allows the user to enter their credentials and location information through various menus/forms and stores the information along with the forecasts in a database.
  - Allows for multiple locations, and retireves/displays forecast for each location in the form of a table
  - Allows for the user to add and remove locations through the corresponding buttons/menus

- webApp version is a Flask app that retrieves the forecast for 329 US Resorts once a day (at 5a.m. in the machines timezone if using the apscheduler) and stores the information 
  in a database.  Users can then view forecast information by various filters
  - If wanting forecast information for a non-resort area (Backcountry) please use another version.
  - Uncomment the apscheduler lines in main.py if not using a task scheduler such as Python Anywhere provides 
  - Unregisterd/Not logged in users can view the forecast for the location with the deepest forecast for the day, as well as the location with the deepest forecast for each of the     major passes (Ikon, Epic, Powder Alliance, Mountain Collective, and Indy).  They can also select one location from a drop down menu to see that location's forecast.
  - Registerd/logged in users can select 4 favorite locations and the passes that they have.  The 4 favorite locations as well as the deepest location for any passes they have
    selected forecasts can then be viewed on the favorites page.
  - Registerd/logged in users can also search/filter by Pass, State, or Reigon which will display the 4 deepest forecasts that match the filter.
  - Live version viewable at https://powderbot.pythonanywhere.com/
