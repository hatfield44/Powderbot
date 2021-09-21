# Methods to populate the dates in the forecast windwo
from datetime import date

# Gets current date and returns it
def getDate():
    currentDate = str(date.today())
    return currentDate[-5:-3] + "/" + currentDate[-2:] + "/" + currentDate[:4]

# Checks for leap year
def checkLeapYear(year):
    if (int(year) % 4 != 0):
        return False
    elif (int(year) % 100 != 0 or int(year) % 400 == 0):
        return True
    else:
        return False

# Increments the day for each day in forecast
def incrementDay(leapYear, dates, month, day, year, i):
     # increment day
    # even months with 30 days
    if (int(month) % 2 == 0 and int(day) < 30 and int(month) != 2):
        dates.append(month + "/" + str(int(day)+i) + "/" + year)
    # odd months with 31 days
    elif (int(month) % 2 == 1 and int(day) < 31 and int(month) != 2):
        dates.append(month + "/" + str(int(day)+i) + "/" + year)
    # feb that odd bastard
    elif (int(month) == 2 and int(day) < 28 and leapYear == False):
        dates.append(month + "/" + str(int(day)+i) + "/" + year)
    # feb in leap year
    elif (int(month) == 2 and int(day) < 29 and leapYear == True):
        dates.append(month + "/" + str(int(day)+i) + "/" + year)


# Increments the Month for each day in forecast in needed
def incrementMonth(leapYear,dates, month, day, year):
    # increment month
    if (int(month)%2 == 0 and int(day) == 30 and int(month) != 2 and int(month) < 12):
        day = 1
        month = int(month) + 1
        dates.append(month + "/" + day + "/" + year)
    elif (int(month)%2 == 1 and int(day) == 31 and int(month) < 12):
        day = 1
        month = int(month) + 1
        dates.append(month + "/" + day + "/" + year)
    elif (int(month) == 2 and int(day) == 28 and leapYear == False):
        day = 1
        month = int(month) + 1
        dates.append(month + "/" + day + "/" + year)
    elif ( int(month)== 2 and int(day) == 29 and leapYear == True):
        day = 1
        month = int(month) + 1
        dates.append(month + "/" + day + "/" + year)


# Increments the year for each day in forecast if needed
def incrementYear(dates, month, day, year):
    # increment year
    if (int(month) == 12 and day == 31):
        month = 1
        day = 1
        year = int(year) + 1
        dates.append(month + "/" + day + "/" + year)

# Returns the list of dates that will be in the forecast
def getDates():
    today = getDate().split("/")
    month = today[0]
    day = today[1]
    year = today[2]
    dates = []

    leapYear = checkLeapYear(year)
    # For each day in the forecast set it's date
    for i in range(10):
        incrementMonth(leapYear,dates, month, day, year)
        incrementDay(leapYear, dates, month, day, year, i)
        incrementYear(dates, month, day, year)
    
    return dates
