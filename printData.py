from pymongo import MongoClient

client = MongoClient()
db = client.DiscordServers

print(list(db.servers.find({})))
