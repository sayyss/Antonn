import datetime

def getAvgMessage(time,totalMsg):

    timeAdded = datetime.datetime.fromtimestamp(time)
    currentTime = datetime.date.today()

    days = timeAdded.date() - currentTime

    return 10

getAvgMessage(1598313600,10)
