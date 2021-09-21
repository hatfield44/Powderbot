#Forecast information provided by 
  #Open Weather  https://home.openweathermap.org/users/sign_up
  #Weather API   https://www.weatherapi.com/signup.aspx
  #Weatherbit    https://www.weatherbit.io/account/create
# Uncomment scheduler lines if needed
# Python anywhere required the use of their task scheduler as apscheduler is not supported
from website import create_app
#from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()
#scheduler = BackgroundScheduler()
if __name__ == '__main__':
    #scheduler.add_job(getForecast, trigger = 'cron', hour = 5)
    #scheduler.start()
    app.run(use_reloader=False)
