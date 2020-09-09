from flask import Flask
from flask import request
from flask import render_template
from operator import itemgetter

import db_commands
import utils
import datetime

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = db_commands.DB()

@app.route("/dashboard", methods=['GET','POST'])
def dashbord():
    
    #if request.method == "POST":
        
    guildID = request.args.get('ID')

    guildData = db.getAll(int(guildID))

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
        return render_template('login.html', name=guildData['name'],id=guildData['id'],password=guildData['password'])

    return render_template("dashboard.html",guildData=guildData,avgMsg=int(avgMsg),members=SortedActiveMem[:10],channels=SortedActiveCha[:10],Msgx=Msgx,Msgy=Msgy,Memx=Memx,Memy=Memy,MsgPie=MsgPie,ChannelPie=ChannelPie)

@app.route("/status", methods=['GET'])
def status():
    print("working")
    return "Working"

@app.route("/testDB",methods=['GET'])
def testDB():

    guildTm = db.getTotalMsgs(710551528301395988)

    return str(guildTm)

@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
