import discord, nhentai, random, requests
from discord.ext import commands
keys={}
nuke=open("nuke.token", "r")
for line in nuke:
    (key,val)=line.split('>')
    keys[key]=val


bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def nukemedaddy(ctx):
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
async def gibcode(ctx, arg):
    doujin=nhentai.get_doujin(int(arg))
    thumb=doujin.thumbnail
    name=doujin.titles['english']
    res = []
    for i in doujin.tags:
        if i[0] not in res and (i != ''):
            res.append(i[2])
    await ctx.send(name+"\n"+thumb+"\n"+str(res))
bot.run(keys['TOKEN'])
