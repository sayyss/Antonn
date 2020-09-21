# imports 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord.utils import find
from operator import itemgetter
import asyncio
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

import db_commands
import utils
import os
import psutil
import time
import datetime
from datetime import timedelta
from dotenv import load_dotenv

# Prefix
bot = commands.Bot(command_prefix="%")
bot.remove_command('help')
bot.load_extension("Stats")


db = db_commands.DB()

load_dotenv()
token = os.getenv('token')

# Events
#***************************************

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="%help"))
    print("Up and Running")

@bot.event
async def on_guild_join(guild):

    guildChannels = utils.getGuildChannels(guild.text_channels)
    guildMembers = utils.getGuildMembers(guild.members)
    
    password = utils.generatePass();

    guildData = {"name": guild.name,
                 "id": guild.id,
                 "total_msg": 0,
                 "total_voice": 0,
                 "channels": guildChannels,
                 "members": guildMembers,
                 "time": datetime.datetime.now().timestamp(),
                 "dailyCount": 0,
                 "dailyVoice": 0,
                 "dailyCounts": [],
                 "memberCounts": [],
                 "voiceCounts": [],
                 "public":True,
                 "password": password}

    db.addServer(guildData)
    #general = find(lambda x: x.name == "general", guild.text_channels)
    
    #await general.send("Hello!! Type %help")

@bot.event
async def on_member_join(member):

    if member.bot:
        return

    newMember = {
    'id': member.id,
    'name': member.display_name,
    'total_msg': 0,
    'voice': 0,
    'voiceState': {'joined': None, 'left': None}
    }
    db.addMember(newMember,member.guild.id)

@bot.event
async def on_guild_channel_create(channel):

    if channel.type == discord.ChannelType.text:

        newChannel = {
            'name': channel.name,
            'id': channel.id,
            'total_msg': 0,
        }
        db.addChannel(newChannel,channel.guild.id)
        print("channel added")

@bot.event
async def on_guild_remove(guild):

    db.removeGuild(guild.id)

@bot.event
async def on_member_remove(member):
    db.removeMember(member.id,member.guild.id)

@bot.event
async def on_guild_channel_delete(channel):
    db.removeChannel(channel.id,channel.guild.id)


# Status getting Passed as Activity, Not Fixed Yet
"""
@bot.event
async def on_member_update(memBefore,memAfter):

    if memAfter.bot:
        return

    if memAfter.activity == None:
        return
    
    validActivity = utils.checkActivitiy(memAfter.activity.type)

    if validActivity:

        if memBefore.activity == None:
            db.updateActivity(memAfter.guild.id, memAfter.activity)
            return


        if memBefore.activity.name != memAfter.activity.name:
            db.updateActivity(memAfter.guild.id, memAfter.activity)
"""

@bot.event
async def on_voice_state_update(member,before,after):

    if before.channel == None:
        if after.channel:
            db.addJoinedTime(member.guild.id,member.id)
    
    if before.channel:
        if after.channel == None:
            db.addLeftTime(member.guild.id,member.id)
    

    if before.channel:
        if after.channel:
            if before.channel.name != after.channel.name:
                db.addJoinedTime(member.guild.id,member.id)

@bot.event
async def on_message(message):

    if message.author.bot:
        return
    db.updateCount(message.guild.id,message.author, message.channel)

    await bot.process_commands(message)


@bot.command(name="help")
async def helpCommand(ctx):

    helpDetails = ""

    helpDetails += "**Prefix: %** \n\n"

    helpDetails += "**General Stats\n\n**"
    helpDetails += "`%stats` - Get Full Stats\n"
    helpDetails += "`%tm` - Get Total Messages\n"
    helpDetails += "`%tm-c` - Get Total Messages of the current channel\n"
    helpDetails += "`%mm <ping@user>` - Get your Total Messages in the server/Get pinged user's total messages in the server\n"
    helpDetails += "`%avg-msg ` - Get Daily Average Messages\n\n"

    helpDetails += "**Web Dashboard**\n\n"
    helpDetails += "`%dashboard` - Get Link to the Web Dashboard\n"
    helpDetails += "`%dashboard-public` - See if Dashboard is Public Or Private\n"
    helpDetails += "`%set-dashboard-public <true/false>` - Set Web Dashboard Public or Private\n\n"

    helpDetails += "**Others**\n\n"
    helpDetails += "`%about` - About Antonn\n"
    helpDetails += "`%invite` - Get Bot Invite Link\n\n"


    helpDetails += "invite - https://bit.ly/3md6zi0\n"
    helpDetails += "Created by **sayyss#9603**"
    embed = discord.Embed(title="Help",description=helpDetails, color=0x00ff40)

    await ctx.send(embed=embed)

@bot.command(name="about")
async def about(ctx):
    
    guildCount = len(bot.guilds)
    userCount = len(bot.users)

    process = psutil.Process()  

    embed = discord.Embed(title="About Antonn", description="Stat Bot",color=0x00ff40)
    embed.add_field(name="**__General Info__**", inline=False, value="\u200b")
    embed.add_field(name="Latency", value=f"{bot.latency*1000:.03f}ms")
    embed.add_field(name="Guild Count", value=guildCount)
    embed.add_field(name="User Count", value=userCount)

    embed.add_field(name="**__Technical Info__**", inline=False, value="\u200b")
    embed.add_field(name="System CPU Usage", value=f"{psutil.cpu_percent():.02f}%")
    embed.add_field(name="System RAM Usage",
                    value=f"{psutil.virtual_memory().used/1048576:.02f} MB")
    embed.add_field(name="System Uptime",
                    value=f'{timedelta(seconds=int(time.time() - psutil.boot_time()))}')
    embed.add_field(name="Bot CPU Usage", value=f"{process.cpu_percent():.02f}%")
    embed.add_field(name="Bot RAM Usage", value=f"{process.memory_info().rss / 1048576:.02f} MB")
    embed.add_field(name="Bot Uptime",
                    value=f'{timedelta(seconds=int(time.time() - process.create_time()))}')

    await ctx.send(embed=embed)

@bot.command(name="invite")
async def invite(ctx):

    link = "https://discord.com/api/oauth2/authorize?client_id=733732900939366427&permissions=8&scope=bot"

    embed = discord.Embed(title="Invite Link",url=link, color=0x00ff40)

    await ctx.send(embed=embed)

bot.run(token)
