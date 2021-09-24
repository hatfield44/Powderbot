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


# Returns the list of dates that will be in the forecast
def getDates():
    today = getDate().split("/")
    month = today[0]
    day = today[1]
    year = today[2]
    leapYear = checkLeapYear(year)
    j = 0
    dates = []

    # For each day in the forecast set it's date

    for i in range(10):
        if (int(month) % 2 == 0 and int(day)+i <= 30 and int(month) != 2):
            dates.append(str(month) + "/" + str(int(day)+i-j) + "/" + year)
        # odd months with 31 days
        elif (int(month) % 2 == 1 and int(day)+i <= 31 and int(month) != 2):
            dates.append(str(month) + "/" + str(int(day)+i-j) + "/" + year)
        # feb that odd bastard
        elif (int(month) == 2 and int(day)+i <= 28 and leapYear == False):
            dates.append(str(month) + "/" + str(int(day)+i-j) + "/" + year)
        # feb in leap year
        elif (int(month) == 2 and int(day)+i <= 29 and leapYear == True):
            dates.append(str(month) + "/" + str(int(day)+i-j) + "/" + year)
        
        if (int(month)%2 == 0 and int(day)+i > 30 and int(month) != 2 and int(month) < 12):
            j=i
            day = 1
            month = int(month) + 1
            dates.append(str(month) + "/" + str(int(day)+i-j) + "/" + year)
        elif (int(month)%2 == 1 and int(day)+i > 31 and int(month) < 12):
            j=i
            day = 1
            month = int(month) + 1
            dates.append(str(month) + "/" + str(int(day)+i-j) + "/" + year)
        elif (int(month) == 2 and int(day)+i > 28 and leapYear == False):
            j=i
            day = 1
            month = int(month) + 1
            dates.append(str(month) + "/" + str(day) + "/" + year)
        elif ( int(month)== 2 and int(day)+i > 29 and leapYear == True):
            j=i
            day = 1
            month = int(month) + 1
            dates.append(str(month) + "/" + str(int(day)+i-j) + "/" + year)

        if (int(month) == 12 and int(day)+i > 31):
                month = 1
                day = 1
                year = int(year) + 1
                dates.append(str(month) + "/" + day + "/" + year)
    
    return dates
