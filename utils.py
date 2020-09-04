import datetime
import matplotlib.pyplot as plt
import numpy as np

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


def getPlot(data):

    x = []
    y = []

    for i in data:

        time = i['time']
        time = datetime.datetime.fromtimestamp(time)
        time = time.date()
        time = str(time)

        x.append(time)
        y.append(i['count'])
    
    return x,y
