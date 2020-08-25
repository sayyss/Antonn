from flask import Flask
from flask import request
from flask import render_template

import db_commands

app = Flask(__name__)

db = db_commands.DB()

@app.route("/dashboard", methods=['GET'])
def dashbord():
    
    guildID = request.args.get('ID')
    guildData = db.getAll(int(guildID))

    return render_template("dashboard.html",guildData=guildData)

if __name__ == '__main__':
    app.run(port=4005)
