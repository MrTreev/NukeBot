import os
import discord, nhentai, random, requests
from discord.ext import commands
fileDir = os.path.dirname(os.path.abspath(__file__))
cursedfile=open(fileDir+"/cursed.tags","r")
cursed=cursedfile.read().splitlines()
cursedfile.close()
bot = commands.Bot(command_prefix='>')
keys={}
nuke=open(fileDir+"/nuke.token", "r")
for line in nuke:
    (key,val)=line.split(' ')
    keys[key]=val
nuke.close()



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
    user=ctx.message.author.id
    server=ctx.guild.id
    add=0
    for tag in res:
        if tag in cursed:
            add=add+1
    print("add="+str(add))
    try:
        userCursed=open(fileDir+"/servers"+"/"+str(server)+"/"+str(user),"r")
        userCursedVal=int(userCursed.readline())
        userCursed.close()
        userCursed=open(fileDir+"/servers"+"/"+str(server)+"/"+str(user),"w")
    except:
        os.mkdir(fileDir+"/servers"+"/"+str(server))
        userCursed=open(fileDir+"/servers"+"/"+str(server)+"/"+str(user),"w")
        userCursed.write("0")
        userCursedVal=0
    cursedMessage="Cursed Value: "+str(add)
    await ctx.send(name+"\n"+thumb+"\n"+code+"\n"+str(res)+"\n"+cursedMessage)
    newCursedVal=str(userCursedVal+add)
    userCursed.write(newCursedVal)
    userCursed.close()



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



@bot.command()
async def checkcurse(ctx):
    user=ctx.message.author.id
    server=ctx.guild.id
    try:
        userCursed=open(fileDir+"/servers"+"/"+str(server)+"/"+str(user),"r")
        userCursedVal=int(userCursed.readline())
        userCursed.close()
        await ctx.send("Your cursed value is: "+str(userCursedVal))
    except:
        await ctx.send("You have no cursed value yet")



@bot.command()
async def cursedtags(ctx):
    cursedText=""
    for tag in cursed:
        cursedText=cursedText+"\n"+tag
    await ctx.send(cursedText)



bot.run(keys['TOKEN'])
