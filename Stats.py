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
import os
import psutil
import time
from datetime import timedelta

db = db_commands.DB()

class Stats(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(pass_context=True, aliases=['tm'])
    async def total_msg(self, ctx):

        totalmsgs = db.getTotalMsgs(ctx.guild.id)

        embedMsg = discord.Embed(title="Total Messages", description=totalmsgs)
        await ctx.send(embed=embedMsg)
    
    @commands.command(pass_context=True, aliases=['tm-c'])
    async def total_msg_channel(self, ctx):
    
        totalmsgs = db.getTotalMsgsChannel(ctx.channel.id,ctx.guild.id)

        embedMsg = discord.Embed(title="Total Messages in #{}".format(ctx.channel.name), description=totalmsgs)
        await ctx.send(embed=embedMsg)
    
    @commands.command(pass_context=True, aliases=['mm'])
    async def my_messages(self, ctx, member: discord.Member = None):

        member = ctx.author if not member else member

        userMsgs = db.getTotalMsgsUser(member.id,ctx.guild.id)

        if not userMsgs:
            await ctx.send("User Not Found")
        
        else:
            embedMsg = discord.Embed(title="{}'s Total Messages in {}".format(member.name,ctx.guild.name), description=userMsgs)
            await ctx.send(embed=embedMsg)

    @commands.command(pass_context=True, aliases=['avg-msg'])
    async def avg_msg(self, ctx):

        totalmsgs = db.getTotalMsgs(ctx.guild.id)
        time = db.getDayAdded(ctx.guild.id)

        avgMsg = utils.getAvgMessage(time,totalmsgs)

        embed = discord.Embed(title="Average Messages Per Day", description=str(int(avgMsg)),color=0x00ff40)

        await ctx.send(embed=embed)

    @commands.command(pass_context=True, name='dashboard')
    async def dashboard(self, ctx):

        state = db.getPublicStatus(ctx.guild.id)

        vc=f"https://antonn.ml/dashboard?ID={ctx.guild.id}"
        embed=discord.Embed(title="Dashboard For {}".format(ctx.guild.name), url=vc, description="", color=0x00ff40)
        
        if not state:
            embed.add_field(name="State",value="Private")

        await ctx.send(embed=embed)
    

    @commands.command(pass_context=True, aliases=['dashboard-public'])
    async def dashboard_public(self, ctx):

        status = db.getPublicStatus(ctx.guild.id)
        await ctx.send(str(status))

    @commands.command(pass_context=True, aliases=['set-dashboard-public'])
    async def set_dashboard_public(self, ctx,state):

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
    

    @commands.command(pass_context=True, name="stats")
    async def stat(self, ctx):

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


def setup(bot):
    bot.add_cog(Stats(bot))
