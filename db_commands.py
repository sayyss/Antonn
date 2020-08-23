from pymongo import MongoClient


class DB:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.DiscordServers
        self.servers = self.db.servers
    
    def addServer(self,guild):
        self.servers.insert_one(guild)
    

    def updateCount(self,guild,user,channel):

        currentGuild = self.servers.find_one({"id":guild})
        currentGuild['total_msg'] += 1
        
        for i in currentGuild['channels']:
            if(i['id'] == channel.id):
                i['total_msg'] += 1
                break
        
        for j in currentGuild['members']:
            if(j['id'] == user.id):
                j['total_msg'] += 1
                break
        
        self.servers.replace_one({"id":guild},currentGuild)
    
    def addMember(self,user,guild):

        currentGuild = self.servers.find_one({"id":guild})
        self.servers.update_one({"id":guild}, {"$set": {"members": currentGuild['members'].append(user)}})
    
    def addChannel(self,channel,guild):

        currentGuild = self.servers.find_one({"id":guild})
        self.servers.update_one({"id":guild}, {"$set": {"channels": currentGuild['channels'].append(channel)}})






    
