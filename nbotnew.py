import os
import discord, nhentai, random, requests
from discord.ext import commands
fileDir = os.path.dirname(os.path.abspath(__file__))
keys={}
nuke=open(fileDir+"/nuke.token", "r")
for line in nuke:
    (key,val)=line.split(' ')
    keys[key]=val


bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def nukemedaddy(ctx):
    await ctx.send("Hacking the NNSA...")
    valid = False
    while valid == False:
        code = ''
        for i in range(6):
            code += str(random.randint(0,9))
        url = 'https://nhentai.net/g/'+code+'/'
        r = requests.get(url)
        if r.status_code != 404:
            valid = True
    doujin=nhentai.get_doujin(int(code))
    name=doujin.titles['english']
    thumb=doujin.thumbnail
    res = []
    for i in doujin.tags:
        if i[0] not in res and (i != ''):
            res.append(i[2])
    await ctx.send(name+"\n"+thumb+"\n"+code+"\n"+str(res))

@bot.command()
async def gib(ctx, *, args):
    if args.isdigit():
        try:
            await ctx.send("processing code...")
            doujin=nhentai.get_doujin(int(args))
            thumb=doujin.thumbnail
            name=doujin.titles['english']
            res = []
            for i in doujin.tags:
                if i[0] not in res and (i != ''):
                    res.append(i[2])
            await ctx.send(name+"\n"+thumb+"\n"+str(res))
        except:
            await ctx.send("unable to fulfil request")
    elif isinstance(args,str):
        try:
            await ctx.send("processing tag...")
            o=1
            ret=[]
            tag=1
            while tag==1:
                listo=nhentai.search(args,o)
                if listo==[]:
                    tag=0
                for i in listo:
                    ret.append(str(i.id))
                o=o+1
            key=random.randint(0,len(ret)-1)
            doujin=nhentai.get_doujin(int(ret[key]))
            name=doujin.titles['english']
            thumb=doujin.thumbnail
            res = []
            for i in doujin.tags:
                if i[0] not in res and (i != ''):
                    res.append(i[2])
            await ctx.send(name+"\n"+thumb+"\n"+ret[key]+"\n"+str(res))
        except:
            await ctx.send("unable to fulfil request")
    else:
        await ctx.send("WTF are you asking for?")

bot.run(keys['TOKEN'])
