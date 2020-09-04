from flask import Flask
from flask import request
from flask import render_template
from operator import itemgetter

import db_commands

app = Flask(__name__)

db = db_commands.DB()

@app.route("/dashboard", methods=['GET'])
def dashbord():
    
    guildID = request.args.get('ID')
    guildData = db.getAll(int(guildID))

    activeMem = guildData['members']
    SortedActiveMem = sorted(activeMem, key=itemgetter('total_msg'), reverse=True)

    activeCha = guildData['channels']
    SortedActiveCha = sorted(activeCha, key=itemgetter('total_msg'), reverse=True)

    members = len(guildData['members'])

    return render_template("dashboard.html",guildData=guildData,activeMembers=SortedActiveMem[:10],activeChannels=SortedActiveCha[:10],members=members)

@app.route("/status", methods=['GET'])
def status():
    print("working")
    return "Working"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
