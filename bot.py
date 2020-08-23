# imports 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord.utils import find
import asyncio

import db_commands

# Prefix
bot = commands.Bot(command_prefix=":")

db = db_commands.DB()

def getGuildChannels(channels):
    guildChannels = []

    for i in channels:
        channel = {
            "name": i.name,
            "id": i.id,
            "total_msg": 0
        }

        guildChannels.append(channel)
    
    return guildChannels

def getGuildMembers(members):

    guildMembers = []

    for i in members:

        if i.bot:
            continue

        member = {
            "id": i.id,
            "name": i.display_name,
            "total_msg": 0,
        }

        guildMembers.append(member)
    
    return guildMembers
     
@bot.event
async def on_ready():
    print("Up and Running")

@bot.event
async def on_guild_join(guild):

    guildChannels = getGuildChannels(guild.text_channels)
    guildMembers = getGuildMembers(guild.members)

    guildData = {"name": guild.name,
                 "id": guild.id,
                 "total_msg": 0,
                 "channels": guildChannels,
                 "members": guildMembers}

    db.addServer(guildData)
    general = find(lambda x: x.name == "general", guild.text_channels)
    
    await general.send("Thanks for Having me Here! type :help")

@bot.event
async def on_member_join(member):

    if member.bot == True:
        newMember = {
        'id': member.id,
        'name': member.display_name,
        'total_msg': 0,
        }
        db.addMember(newMember,member.guild.id)

@bot.event
async def on_guild_channel_create(channel):
    
    newChannel = {
        'name': channel.name,
        'id': channel.id,
        'total_msg': 0
    }
    db.addChannel(newChannel,channel.guild.id)

@bot.event
async def on_guild_remove(guild):

    db.removeGuild(guild.id)

@bot.event
async def on_member_remove(member):
    db.removeMember(member.id,member.guild.id)

@bot.event
async def on_message(message):
    db.updateCount(message.guild.id,message.author, message.channel)

bot.run("NzMzNzMyOTAwOTM5MzY2NDI3.XxHcRQ.w1zFRC4l3Yms7UdO_q0FkY5wxcI")