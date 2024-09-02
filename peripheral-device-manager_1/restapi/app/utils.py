# write log
from datetime import datetime

# write log
def WriteLog(message):
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    f = open('C:\logfiles\DeviceManager\DeviceManager.log','a+')
    f.write("{};{}\n".format(date_time, message))
    f.close()
