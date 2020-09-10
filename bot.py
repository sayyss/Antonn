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
from datetime import timedelta

# Prefix
bot = commands.Bot(command_prefix="%")
bot.remove_command('help')

db = db_commands.DB()


# Events
#***************************************
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
    
    password = utils.generatePass();

    guildData = {"name": guild.name,
                 "id": guild.id,
                 "total_msg": 0,
                 "channels": guildChannels,
                 "members": guildMembers,
                 "time": datetime.datetime.now().timestamp(),
                 "dailyCount": 0,
                 "dailyCounts": [],
                 "memberCounts": [],
                 "public":True,
                 "password": password}

    db.addServer(guildData)
    general = find(lambda x: x.name == "general", guild.text_channels)
    
    await general.send("Hello!! Type %help")

@bot.event
async def on_member_join(member):

    if member.bot:
        return

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

@bot.event
async def on_message(message):

    if message.author.bot:
        return
    db.updateCount(message.guild.id,message.author, message.channel)

    await bot.process_commands(message)

#********************************************

# Commands

@bot.command(name="tm")
async def total_msg(ctx):

    totalmsgs = db.getTotalMsgs(ctx.guild.id)

    embedMsg = discord.Embed(title="Total Messages", description=totalmsgs)
    await ctx.send(embed=embedMsg)


@bot.command(name="tm-c")
async def total_msg_channel(ctx):
    
    totalmsgs = db.getTotalMsgsChannel(ctx.channel.id,ctx.guild.id)

    embedMsg = discord.Embed(title="Total Messages in #{}".format(ctx.channel.name), description=totalmsgs)
    await ctx.send(embed=embedMsg)

@bot.command(name="mm")
async def my_messages(ctx, member: discord.Member = None):

    member = ctx.author if not member else member

    userMsgs = db.getTotalMsgsUser(member.id,ctx.guild.id)

    if not userMsgs:
        await ctx.send("User Not Found")
    
    else:
        embedMsg = discord.Embed(title="{}'s Total Messages in {}".format(member.name,ctx.guild.name), description=userMsgs)
        await ctx.send(embed=embedMsg)


@bot.command(name="avg-msg")
async def avg_msg(ctx):

    totalmsgs = db.getTotalMsgs(ctx.guild.id)
    time = db.getDayAdded(ctx.guild.id)

    avgMsg = utils.getAvgMessage(time,totalmsgs)

    embed = discord.Embed(title="Average Messages Per Day", description=str(int(avgMsg)),color=0x00ff40)

    await ctx.send(embed=embed)

@bot.command(name="dashboard")
async def dashboard(ctx):

    state = db.getPublicStatus(ctx.guild.id)

    vc=f"https://antonn.ml/dashboard?ID={ctx.guild.id}"
    embed=discord.Embed(title="Dashboard For {}".format(ctx.guild.name), url=vc, description="", color=0x00ff40)
    
    if not state:
        embed.add_field(name="State",value="Private")

    await ctx.send(embed=embed)

@bot.command(name="dashboard-public")
async def dashboard_public(ctx):

    status = db.getPublicStatus(ctx.guild.id)

    await ctx.send(str(status))

@bot.command(name="set-dashboard-public")
async def set_dashboard_public(ctx,state):

    if state == "true" or state == "True":
        public = True
        db.setPublicStatus(ctx.guild.id,public)


        await ctx.send("Dashboard is now Public")
        return

    if state == "false" or state == "False":
        public = False
        db.setPublicStatus(ctx.guild.id,public)

        await ctx.send("Dashboard is now Private")
        return
    
    else:
        await ctx.send("Retry the command with either True or False")


@bot.command(name="stat")
async def stat(ctx):

    link=f"https://antonn.ml/dashboard?ID={ctx.guild.id}"

    guildData = db.getAll(ctx.guild.id)

    avgMsg = utils.getAvgMessage(guildData['time'],guildData['total_msg'])

    activeMem = guildData['members']
    SortedActiveMem = sorted(activeMem, key=itemgetter('total_msg'), reverse=True)

    activeCha = guildData['channels']
    SortedActiveCha = sorted(activeCha, key=itemgetter('total_msg'), reverse=True)

    description_names = ""
    description_msgs = ""

    for i in SortedActiveMem[:10]:
        member = ctx.guild.get_member(i['id'])
        description_names += "{}\n".format(member.mention)

    for i in SortedActiveMem[:10]:
        description_msgs += "{}\n".format(i['total_msg'])

    description_names2 = ""
    description_msgs2 = ""

    for i in SortedActiveCha[:10]:
        channel = ctx.guild.get_channel(i['id'])
        description_names2 += "{}\n".format(channel.mention)

    for i in SortedActiveCha[:10]:
        description_msgs2 += "{}\n".format(i['total_msg'])

    embed = discord.Embed(title="Stats For {}".format(ctx.guild.name),url=link, colour=0xF70D02)

    
    embed.add_field(name="Messages", value=guildData['total_msg'])
    embed.add_field(name="Avg Messages", value=round(avgMsg))
    embed.add_field(name="Today", value=guildData['dailyCount'])

    
    embed.add_field(name="Active Members\n\n", value=description_names)
    embed.add_field(name="Messages\n\n", value=description_msgs)
    embed.add_field(name="Members", value=len(guildData['members']))

    
    embed.add_field(name="Active Channels\n\n", value=description_names2)
    embed.add_field(name="Messages\n\n", value=description_msgs2)
    embed.add_field(name="Channels", value=len(guildData['channels']))

    embed.add_field(name="__Dashboard__",value=link)

    if not guildData['public']:
        embed.add_field(name="Dashboard State",value="Private")


    await ctx.send(embed=embed)

@bot.command(name="help")
async def helpCommand(ctx):

    helpDetails = ""

    helpDetails += "**Prefix: %** \n\n"

    helpDetails += "**General Stats\n**"
    helpDetails += "`%stat` - Get Stats\n"
    helpDetails += "`%tm` - Get Total Messages\n"
    helpDetails += "`%tm-c` - Get Total Messages of the current channel\n"
    helpDetails += "`%mm` - Get your Total Messages in the server\n\n"

    helpDetails += "**Analytics**\n"

    embed = discord.Embed(title="Help",description=helpDetails, colour=0xF70D02)

    await ctx.send(embed=embed)

@bot.command(name="about")
async def about(ctx):

    guildCount = len(bot.guilds)
    userCount = len(bot.users)

    process = psutil.Process()  

    embed = discord.Embed(title="About Antonn", description="Stat Bot",color=0xF70D02)
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
bot.run("NzMzNzMyOTAwOTM5MzY2NDI3.XxHcAw.xlAhbCfnwrcDWumQXvPCOWC8g0U")
