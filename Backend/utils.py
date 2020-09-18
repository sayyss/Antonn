import datetime
import matplotlib.pyplot as plt
import numpy as np
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_ENDPOINT = 'https://discord.com/api/v6'
REDIRECT_URI = 'localhost:8000/user'
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def exchange_code(code):

  data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI,
    'scope': 'Know what Servers the user is in'
  }

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
  r.raise_for_status()
  return r.json()

def getUserData(access_token):
    
    headers = {
        'Authorization': "Bearer {}".format(access_token)
    }
    guilds = requests.get("https://discord.com/api/users/@me/guilds",headers=headers)
    guilds = guilds.json()

    user = requests.get("https://discord.com/api/users/@me",headers=headers)
    user = user.json()

    return user,guilds


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

def preprocessPlot(data,count,date):

    x = []
    y = []

    if not data:
        x = ['0',date]
        y = [0,count]

    else:
        x,y = getPlot(data)
        x.append(date)
        y.append(count)
    
    return x,y

def timestamp_to_date(time):

    date = datetime.datetime.fromtimestamp(time)
    date = date.date()
    date = str(date)

    return date
