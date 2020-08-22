from pymongo import MongoClient


class DB:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.DiscordServers
    
    def addServer(self,guild):
        servers = self.db.servers
        servers.insert_one(guild)


    
