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
bot.load_extension("Stats")

db = db_commands.DB()


# Events
#***************************************

@bot.event
async def on_ready():
    print("Up and Running")

@bot.event
async def on_guild_join(guild):

    guildChannels = utils.getGuildChannels(guild.text_channels)
    guildMembers = utils.getGuildMembers(guild.members)
    
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
