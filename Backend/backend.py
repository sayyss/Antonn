from flask import Flask, request,redirect, url_for, render_template
from flask import session as login_session
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from operator import itemgetter
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

import db_commands
import utils
import datetime
import requests

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'atonnnnnnnnnnnnnnnnnnnnnnnn'

API_ENDPOINT = 'https://discord.com/api/v6'
CLIENT_ID = '733732900939366427'
CLIENT_SECRET = 'pSmqJLZNtLihB-bcHuXsYT0o9Mpw-v_I'
REDIRECT_URI = 'https://antonn.ml/user/'

db = db_commands.DB()

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

@app.route("/dashboard", methods=['GET','POST'])
def dashboard():

    guildID = request.args.get('ID')
    guildData = db.getAll(int(guildID))

    if not guildData:
        return render_template("error.html",logged_in=None, serverExist=False)
        
    avgMsg = utils.getAvgMessage(guildData['time'],guildData['total_msg'])

    activeMem = guildData['members']
    SortedActiveMem = sorted(activeMem, key=itemgetter('total_msg'), reverse=True)

    activeCha = guildData['channels']
    SortedActiveCha = sorted(activeCha, key=itemgetter('total_msg'), reverse=True)

    # Messages Graph Data
    Msgdata = db.getDailyMsgs(int(guildID))

    count = guildData['dailyCount']
    date = utils.timestamp_to_date(datetime.datetime.today().timestamp())

    Msgx,Msgy = utils.preprocessPlot(Msgdata,count,date)

    # Members Graph data
    Memdata = db.getDailyMem(int(guildID))
    Memx,Memy = utils.getPlot(Memdata)

    #Msg Pie data
    MsgPie = SortedActiveMem[:10]
    ActiveSum = sum(mem['total_msg'] for mem in SortedActiveMem[:10])

    total = {
        "name": "others",
        "total_msg": guildData['total_msg'] - ActiveSum
    }
    
    MsgPie.append(total)

    #Channel Pie data
    ChannelPie = SortedActiveCha[:10]
    ActiveSumCh = sum(channel['total_msg'] for channel in SortedActiveCha[:10])

    totalCh = {
        "name": "others",
        "total_msg": guildData['total_msg'] - ActiveSumCh
    }

    ChannelPie.append(totalCh)

    if not guildData['public']:
        if "token" in login_session:

            userID = login_session['userID']

            checkUserinGuild = db.checkUserinGuild(guildData['id'],userID)
            if checkUserinGuild:
                return render_template("dashboard.html",guildData=guildData,avgMsg=int(avgMsg),members=SortedActiveMem[:10],channels=SortedActiveCha[:10],Msgx=Msgx,Msgy=Msgy,Memx=Memx,Memy=Memy,MsgPie=MsgPie,ChannelPie=ChannelPie)
            else:
                return render_template("error.html",logged_in=True)
        
        else:
            return redirect(url_for("login"))

    return render_template("dashboard.html",guildData=guildData,avgMsg=int(avgMsg),members=SortedActiveMem[:10],channels=SortedActiveCha[:10],Msgx=Msgx,Msgy=Msgy,Memx=Memx,Memy=Memy,MsgPie=MsgPie,ChannelPie=ChannelPie)


@app.route("/login")
def login():
    return redirect("https://discord.com/api/oauth2/authorize?client_id=733732900939366427&redirect_uri=https%3A%2F%2Fantonn.ml%2Fuser%2F&response_type=code&scope=identify%20guilds")

@app.route("/user/")
def user():

    if 'token' in login_session:

        access_token = login_session['token']
        user,guilds = getUserData(access_token)

        if 'userID' not in login_session:
            login_session['userID'] = user['id']

        antonnGuilds = db.checkGuilds(guilds)

        return render_template("user.html",guilds=antonnGuilds,user=user,token=access_token)

    args = request.args

    if not args:
        return redirect(url_for("login"))

    code = args['code']
    responseJson = exchange_code(code);
    
    access_token = responseJson['access_token']
    login_session['token'] = access_token

    user,guilds = getUserData(access_token)
    login_session['userID'] = user['id']

    antonnGuilds = db.checkGuilds(guilds)

    return render_template("user.html",guilds=antonnGuilds,user=user,token=access_token)


@app.route("/testDB",methods=['GET'])
def testDB():

    guildTm = db.getTotalMsgs(710551528301395988)

    return str(guildTm)

@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
