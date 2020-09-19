import schedule
import time
from pymongo import MongoClient
import datetime

def updateCount():

    client = MongoClient()
    db = client.DiscordServers
    servers = db.servers

    result = db.servers.find({})

    for server in result:
        dailyCount = server['dailyCount']
        newDaily = {
           "time": int(datetime.datetime.now().timestamp()),
           "count": dailyCount
        }
        server['dailyCounts'].append(newDaily)
        server['dailyCount'] = 0

        members = server['members']
        memberCount = len(members)
        
        newMember = {
           "time": int(datetime.datetime.now().timestamp()),
           "count": memberCount
        }

        server['memberCounts'].append(newMember)

        voiceCount = server['dailyVoice']
        newVoice = {
           "time": int(datetime.datetime.now().timestamp()),
           "count": voiceCount
        }

        server['voiceCounts'].append(newVoice)
        server['dailyVoice'] = 0

        servers.replace_one({"id":server['id']},server)


schedule.every().day.at("23:58").do(updateCount)

while True:
    schedule.run_pending()
    time.sleep(1)