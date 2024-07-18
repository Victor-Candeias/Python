#
# Example file for working with date information
# LinkedIn Learning Python course by Joe Marini
#

from datetime import date
from datetime import time
from datetime import datetime

def main():
    ## DATE OBJECTS
    # TODO: Get today's date from the simple today() method from the date class
    # today = date.today()
    # print("Today's date is", today)

    # TODO: print out the date's individual components
    # print("Date components:", today.day, today.month, today.year)
    
    # TODO: retrieve today's weekday (0=Monday, 6=Sunday)
    # print("Today's weekday number is ", today.weekday())
    # days = ["seguanda", "terça", "quarta", "quinta", "sexta", "sabado", "domingo"]
    
    # print("Which is", days[today.weekday()])
    
    ## DATETIME OBJECTS
    # TODO: Get today's date from the datetime class
    today = datetime.now()
    print("The current date time is", today)
    
    # TODO: Get the current time
    t = datetime.time(datetime.now())
    print("Current time is", t)

 

  
if __name__ == "__main__":
    main()
  