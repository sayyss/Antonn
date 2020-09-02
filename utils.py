import datetime

def getAvgMessage(time,totalMsg):

    timeAdded = datetime.datetime.fromtimestamp(time)
    currentTime = datetime.date.today()

    timeAdded = datetime.date(timeAdded.year,timeAdded.month,timeAdded.day)
    currentTime = datetime.date(currentTime.year,currentTime.month,currentTime.day)

    days = currentTime - timeAdded

    if days.days == 0:
        return totalMsg

    else:
        return totalMsg/days.days