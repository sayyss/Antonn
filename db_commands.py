from pymongo import MongoClient


class DB:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.DiscordServers
        self.servers = self.db.servers
    
    def addServer(self,guild):
        self.servers.insert_one(guild)

    def removeGuild(self,guild):
        self.servers.delete_one({'id':guild})

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
        newMembers = currentGuild['members'].append(user)

        self.servers.update_one({'id':guild}, {'$set': {'members': newMembers}})
    
    def removeMember(self,member,guild):

        currentGuild = self.servers.find_one({"id":guild})
        currentMembers = currentGuild['members']

        newMembers = [i for i in currentMembers if not (i['id'] == member)]

        self.servers.update_one({'id':guild}, {'$set': {'members': newMembers}})
        
    def addChannel(self,channel,guild):

        currentGuild = self.servers.find_one({"id":guild})
        currentGuild['channels'].append(channel)

