import datetime
import matplotlib.pyplot as plt
import numpy as np
import random
import string

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

def getDaysSinceAdded(time):

    timeAdded = datetime.datetime.fromtimestamp(time)
    currentTime = datetime.date.today()

    timeAdded = datetime.date(timeAdded.year,timeAdded.month,timeAdded.day)
    currentTime = datetime.date(currentTime.year,currentTime.month,currentTime.day)

    days = currentTime - timeAdded

    return days.days

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


def timestamp_to_date(time):

    date = datetime.datetime.fromtimestamp(time)
    date = date.date()
    date = str(date)

    return date

def generatePass():

    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(20)))

    return result_str

def getGuildChannels(channels):
    guildChannels = []

    for i in channels:
        channel = {
            "name": i.name,
            "id": i.id,
            "total_msg": 0
        }

        guildChannels.append(channel)
    
    return guildChannels

def getGuildMembers(members):

    guildMembers = []

    for i in members:

        if i.bot:
            continue

        member = {
            "id": i.id,
            "name": i.display_name,
            "total_msg": 0,
        }

        guildMembers.append(member)
    
    return guildMembers