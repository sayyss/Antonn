# imports 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord.utils import find
import asyncio

# Prefix
bot = commands.Bot(command_prefix=":")

@bot.event
async def on_ready():
    print("Hello")

@bot.event
async def on_guild_join(guild):

    
    general = find(lambda x: x.name == "general", guild.text_channels)

    await general.send("Hello, thanks for adding me")
    
bot.run("NzMzNzMyOTAwOTM5MzY2NDI3.XxHcRQ.w1zFRC4l3Yms7UdO_q0FkY5wxcI")