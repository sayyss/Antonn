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

@app.route("/dashboard", methods=['GET'])
def dashbord():
    
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

    return render_template("dashboard.html",guildData=guildData,avgMsg=int(avgMsg),members=SortedActiveMem[:11],channels=SortedActiveCha[:11],Msgx=Msgx,Msgy=Msgy,Memx=Memx,Memy=Memy)

@app.route("/status", methods=['GET'])
def status():
    print("working")
    return "Working"

@app.route("/testDB",methods=['GET'])
def testDB():

    guildTm = db.getTotalMsgs(710551528301395988)

    return str(guildTm)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
