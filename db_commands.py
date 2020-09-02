from pymongo import MongoClient
import os
import datetime
import time

class DB:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.DiscordServers
        self.servers = self.db.servers
        
    
    #**********************
    # Read Functions

    def getAll(self,guild):
        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild

    def getTotalMsgs(self,guild):

        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild['total_msg']

    def getDailyMsgs(self,guild):

        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild['dailyCounts']

    def getTotalMsgsChannel(self,channel,guild):
        currentGuild = self.servers.find_one({"id":guild})

        for i in currentGuild['channels']:
            if i['id'] == channel:
                return i['total_msg']
    
    def getTotalMsgsUser(self,user,guild):

        currentGuild = self.servers.find_one({"id":guild})
        
        for i in currentGuild['members']:
            if i['id'] == user:
                return i['total_msg']
    
    def getAllMemberMsgs(self,guild):

        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild['members']
    
    def getAllChannelMsgs(self,guild):

        currentGuild = self.servers.find_one({"id": guild})
        return currentGuild['channels']
        
    def addServer(self,guild):
        self.servers.insert_one(guild)

    def removeGuild(self,guild):
        self.servers.delete_one({'id':guild})

    def updateDailyCount(self,guild):
        
       
       currentGuild = self.servers.find_one({"id":guild})
       dailyCount = currentGuild['dailyCount']

       newDaily = {
           "time": datetime.datetime.now().timestamp(),
           "count": dailyCount
       }

       currentGuild['dailyCounts'].append(newDaily)
       
       self.servers.replace_one({"id":guild},currentGuild)

    def updateCount(self,guild,user,channel):

        

        #tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        #today = datetime.date.today()

        currentGuild = self.servers.find_one({"id":guild})
        currentGuild['total_msg'] += 1
        currentGuild['dailyCount'] += 1
        
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
        currentGuild['members'].append(user)

        self.servers.replace_one({"id":guild},currentGuild)
    
    def removeMember(self,member,guild):

        currentGuild = self.servers.find_one({"id":guild})
        currentMembers = currentGuild['members']

        newMembers = [i for i in currentMembers if not (i['id'] == member)]
        currentGuild['members'] = newMembers

        self.servers.replace_one({"id":guild},currentGuild)
        
    def addChannel(self,channel,guild):

        currentGuild = self.servers.find_one({"id":guild})
        currentGuild['channels'].append(channel)

        self.servers.replace_one({"id":guild},currentGuild)
    
    def removeChannel(self,channel, guild):

        currentGuild = self.servers.find_one({"id":guild})
        currentChannels = currentGuild['channels']

        newChannels = [i for i in currentChannels if not (i['id'] == channel)]
        currentGuild['channels'] = newChannels

        self.servers.replace_one({"id":guild},currentGuild)
