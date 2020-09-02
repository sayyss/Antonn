# imports 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord.utils import find
from operator import itemgetter
import asyncio
import datetime

import db_commands
import utils

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

    guildData = {"name": guild.name,
                 "id": guild.id,
                 "total_msg": 0,
                 "channels": guildChannels,
                 "members": guildMembers,
                 "time": datetime.datetime.now().timestamp()}

    db.addServer(guildData)
    general = find(lambda x: x.name == "general", guild.text_channels)
    
    await general.send("Hello Degenerates!!")

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
async def my_messages(ctx):

    totalmsgs = db.getTotalMsgsUser(ctx.author.id,ctx.guild.id)

    embedMsg = discord.Embed(title="Your Total Messages in {}".format(ctx.guild.name), description=totalmsgs)
    await ctx.send(embed=embedMsg)

@bot.command(name="stat")
async def stat(ctx):

    totalmsgs = db.getTotalMsgs(ctx.guild.id)

    guildData = db.getAll(ctx.guild.id)

    avgMsg = utils.getAvgMessage(guildData['time'],totalmsgs)
    

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

    embed = discord.Embed(title="Stats For {}".format(ctx.guild.name),description="**Still in Development**\n\n", colour=0xF70D02)

    
    embed.add_field(name="Messages", value=totalmsgs)
    embed.add_field(name="Avg Messages", value=round(avgMsg))
    embed.add_field(name="Avg Messages", value="soon")
    embed.add_field(name="Active Members\n\n", value=description_names)
    embed.add_field(name="Messages\n\n", value=description_msgs)
    embed.add_field(name="Members", value=len(guildData['members']))

    embed.add_field(name="Active Channels\n\n", value=description_names2)
    embed.add_field(name="Messages\n\n", value=description_msgs2)
    embed.add_field(name="Channels", value=len(guildData['channels']))


    await ctx.send(embed=embed)
bot.run("NzMzNzMyOTAwOTM5MzY2NDI3.XxHcRQ.w1zFRC4l3Yms7UdO_q0FkY5wxcI")