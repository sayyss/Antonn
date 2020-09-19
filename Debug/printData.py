from pymongo import MongoClient

client = MongoClient()
db = client.DiscordServers

servers = db.servers.find({})

for i in servers:
	print(i)
	print("\n")
