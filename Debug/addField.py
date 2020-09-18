from pymongo import MongoClient
client = MongoClient()

db = client.DiscordServers
servers = db.servers
result = db.servers.find({})


for server in result:
    """
    voiceState = {'joined': None, 'left': None }
    for member in server['members']:
       #member['voiceState'] = voiceState
       #member['voice'] = 0
    """

    server['total_voice'] = 0

    servers.replace_one({'id':server['id']},server)

    
