"""

Contains all the commands that were killled

"""

@bot.command(name="mem-graph")
async def member_plot(ctx):

    data = db.getDailyMem(ctx.guild.id)
    x,y = utils.getPlot(data)

    plt.style.use('dark_background')
    plt.figure(figsize=(25,8))
    plt.title("Members every Day")
    plt.xlabel("Time")
    plt.ylabel("Num of Members")
    plt.plot(x,y)
    plt.savefig(fname="plot2")

    await ctx.send(file=discord.File('plot2.png'))
    os.remove('plot2.png')

    
@bot.command(name="msg-graph")
async def message_plot(ctx):

    data = db.getDailyMsgs(ctx.guild.id)
    guildData = db.getAll(ctx.guild.id)

    count = guildData['dailyCount']
    date = utils.timestamp_to_date(datetime.datetime.today().timestamp())

    if not data:
        x = ['0',date]
        y = [0,count]

        ax = plt.figure().gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
        plt.style.use('dark_background')
        plt.title("Messages every Day")
        plt.xlabel("Time")
        plt.ylabel("Num of Messages")
        plt.plot(x,y)

        plt.savefig(fname="plot")
        await ctx.send(file=discord.File('plot.png'))

        os.remove('plot.png')
        return
    

    x,y = utils.getPlot(data)

    x.append(date)
    y.append(count)

    plt.style.use('dark_background')
    plt.figure(figsize=(25,8))
    plt.title("Messages every Day")
    plt.xlabel("Time")
    plt.ylabel("Num of Messages")
    plt.plot(x,y)
    plt.savefig(fname="plot")

    await ctx.send(file=discord.File('plot.png'))
    os.remove('plot.png')