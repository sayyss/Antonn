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
    
    def getMemberByID(self,userID,guild):

        currentGuild = self.servers.find_one({"id":guild})
        
        for i in currentGuild['members']:
            if i['id'] == userID:
                return i;

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

    def setPublicStatus(self,guild,state):

        currentGuild = self.servers.find_one({"id":guild})
        currentGuild['public'] = state

        self.servers.replace_one({"id":guild},currentGuild)
        
    def addServer(self,guild):
        self.servers.insert_one(guild)

    def removeGuild(self,guild):
        self.servers.delete_one({'id':guild})

    def updateName(self,userID,guild,newName):
        currentGuild = self.servers.find_one({"id":guild})

        for i in currentGuild['members']:
            if i['id'] == userID:
                i['name'] = newName
                break
        
        self.servers.replace_one({"id":guild},currentGuild)
    
    def updateActivity(self,guild,activity):
        
        currentGuild = self.servers.find_one({"id":guild})

        exist = False

        if activity:

            for i in currentGuild['activities']:
                if i['name'] == activity.name:
                    exist = True
                    i['count'] += 1
            
            if exist == False:
                activity = {
                    'name': activity.name,
                    'count': 1
                }

                currentGuild['activities'].append(activity)
        
        self.servers.replace_one({"id":guild},currentGuild)

    def updateCount(self,guild,user,channel):

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
    
    def addJoinedTime(self,guild,userID):

        timestamp = datetime.datetime.today().timestamp()

        currentGuild = self.servers.find_one({"id":guild})

        for i in currentGuild['members']:

            if i['id'] == userID:
                voiceState = i['voiceState']
                voiceState['joined'] = None

                if voiceState['joined'] == None:
                    voiceState['joined'] = timestamp
                    break
                else:
                    break
        
        self.servers.replace_one({"id":guild},currentGuild)

    def addLeftTime(self,guild,userID):

        timestamp = datetime.datetime.today().timestamp()

        currentGuild = self.servers.find_one({"id":guild})

        for i in currentGuild['members']:

            if i['id'] == userID:
                voiceState = i['voiceState']

                if voiceState['left'] == None:
                    timeBefore = voiceState['joined']

                    time = timestamp - timeBefore
                    i['voice'] += time
                    currentGuild['total_voice'] += time
                    currentGuild['dailyVoice'] += time
                    
                    voiceState['joined'] = None

                    break
                else:
                    break
    
        self.servers.replace_one({"id":guild},currentGuild)

    