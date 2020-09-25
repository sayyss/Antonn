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

    def getID(self,id):
        currentGuild = self.servers.find_one({"_id":id})
        return currentGuild['id']

    def getDocID(self,id):
        currentGuild = self.servers.find_one({"id":id})
        return currentGuild['_id']

    def getAll(self,guild):
        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild

    def getTotalMsgs(self,guild):

        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild['total_msg']

    def getDailyMsgs(self,guild):

        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild['dailyCounts']
    
    def getDailyMem(self,guild):

        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild['memberCounts']

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
    
    def getIDByName(self,username,guild):
        
        currentGuild = self.servers.find_one({"id":guild})

        for i in currentGuild['members']:
            if i['name'] == username:
                return i['id']
    
    def getAllMemberMsgs(self,guild):

        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild['members']
    
    def getAllChannelMsgs(self,guild):

        currentGuild = self.servers.find_one({"id": guild})
        return currentGuild['channels']

    def getDayAdded(self,guild):

        currentGuild = self.servers.find_one({"id": guild})
        return currentGuild['time']
        

    def getPublicStatus(self,guild):

        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild['public']

    
    def getPassword(self,guild):

        currentGuild = self.servers.find_one({"id":guild})
        return currentGuild['password']
    
    def checkGuilds(self,guilds):

        antonnGuilds = []

        if not guilds:
            return None
            
        for guild in guilds:
            guildID = guild['id']
            currentGuild = self.servers.find_one({"id":int(guildID)})
            if currentGuild:
                antonnGuilds.append(guild)
        
        return antonnGuilds
    
    def checkUserinGuild(self,guild,userID):
        currentGuild = self.servers.find_one({"id":guild})
        
        for member in currentGuild['members']:
            if member['id'] == int(userID):
                return True
    
    def getVoiceData(self,guild):
        currentGuild = self.servers.find_one({"id":guild})

        return currentGuild['voiceCounts']

