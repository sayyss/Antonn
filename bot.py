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
bot = commands.Bot(command_prefix=":")

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
    
    await general.send("Thanks for Having me Here! type :help")

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

@bot.command(name="total-messages")
async def total_msg(ctx):

    totalmsgs = db.getTotalMsgs(ctx.guild.id)

    embedMsg = discord.Embed(title="Total Messages", description=totalmsgs)
    await ctx.send(embed=embedMsg)


@bot.command(name="total-messages-channel")
async def total_msg_channel(ctx):
    
    totalmsgs = db.getTotalMsgsChannel(ctx.channel.id,ctx.guild.id)

    embedMsg = discord.Embed(title="Total Messages in #{}".format(ctx.channel.name), description=totalmsgs)
    await ctx.send(embed=embedMsg)

@bot.command(name="my-messages")
async def my_messages(ctx):

    totalmsgs = db.getTotalMsgsUser(ctx.author.id,ctx.guild.id)

    embedMsg = discord.Embed(title="Your Total Messages in {}".format(ctx.guild.name), description=totalmsgs)
    await ctx.send(embed=embedMsg)

@bot.command(name="stat")
async def stat(ctx):

    totalmsgs = db.getTotalMsgs(ctx.guild.id)
    memberMsgs = db.getAllMemberMsgs(ctx.guild.id)
    channelMsgs = db.getAllChannelMsgs(ctx.guild.id)

    totalMembers = len(memberMsgs)
    totalTextChannels = len(ctx.guild.text_channels)
    totalVoiceChannels = len(ctx.guild.voice_channels)

    guildData = db.getAll(ctx.guild.id)

    avgMsg = utils.getAvgMessage(guildData['time'],totalmsgs)
    

    activeMem = guildData['members']
    SortedActiveMem = sorted(activeMem, key=itemgetter('total_msg'), reverse=True)

    activeCha = guildData['channels']
    SortedActiveCha = sorted(activeCha, key=itemgetter('total_msg'), reverse=True)

    description = "\n\n"

    for i in SortedActiveMem[:10]:
        description += "----------------------\n"
        description += "{} {}\n".format(i['name'],i['total_msg'])

    description += "\n\n"

    description2 = ""

    for i in SortedActiveCha[:10]:
        description2 += "----------------------\n"
        description2 += "{} {}\n".format(i['name'],i['total_msg'])

    embed = discord.Embed(title="Stats For {}".format(ctx.guild.name),description="Test\n\n", colour=0xF70D02)

    embed.add_field(name="Messages", value=totalmsgs)
    embed.add_field(name="Avg Messages", value=totalVoiceChannels)
    embed.add_field(name="Members", value=totalMembers)
    embed.add_field(name="Text Channels", value=totalTextChannels)
    embed.add_field(name="Voice Channels", value=totalVoiceChannels)
    embed.add_field(name="Voice Channels", value=totalVoiceChannels)
    embed.add_field(name="Active Members", value=description)
    embed.add_field(name="Active Channels", value=description2)


    await ctx.send(embed=embed)
bot.run("NzMzNzMyOTAwOTM5MzY2NDI3.XxHcRQ.w1zFRC4l3Yms7UdO_q0FkY5wxcI")