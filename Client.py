import discord
from discord.ext import commands
from Rapper import Rapper
import json
import string
import os
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from dacite import from_dict

class ClientCog(commands.Cog):
    def __init__(self, bot):
        self.users = loadUserData()
        self.bot = bot

    #rap
    #makes money based on quality of current music
    @commands.command(name='rap')
    async def rap(self, ctx):
        self.insertNewUser(ctx.author, False)
        u = self.users[ctx.author.id]
        u.addMoney(100)
        await ctx.send('**'+ctx.author.name+'**\nYou rap really good and make some money.\nNew balance: ' + str(u.money))
        saveUserData(self.users)

    #smoke N
    #automatically smokes N grams of highest tier strain
    @commands.command(name='smoke')
    async def smoke(self, ctx, arg:int):
        await ctx.send('You smoke fat ' + str(arg) + " Gs straight down the drain my guy")

    #buy N [strain]
    #buys up to N grams of selected strain
    #if N*cost>money, buys as much as possible
    @commands.command(pass_context = True , aliases=['weed', 'kush', 'loud', 'dank', 'marijuana', 'cannabis', 'ganja', 'ganj'])
    async def buy(self, ctx, *args):
        strains = parseJSON("strains")
        if len(args) == 0:  
            tosend = ""
            for n in strains["strains"]:
                tosend+=("\n"+n["name"] + ": $" + str(n["price"]) + "/g")
            await ctx.send("welcome to the weed shop. here are our strains:"+tosend)
        elif len(args) >= 2:
            
            sname = ""
            for i in range(1, len(args)):
                sname += (args[i] + " ")
            sname = sname[:-1]

            for strain in strains["strains"]:
                if sname.upper() == strain["name"].upper():
                    self.insertNewUser(ctx.author, False)
                    u = self.users[ctx.author.id]
                    
                    if u.money >= int(args[0]) * int(strain["price"]):
                        u.addMoney(-1*int(args[0]) * int(strain["price"]))
                        u.addWeed(strain["name"], int(args[0]))
                        saveUserData(self.users)
                        await ctx.send("you bought "+str(args[0])+" Gs for $" + str(int(args[0])*int(strain["price"]))+"\nyou now have " + str(u.weed[strain["name"]]) + " Gs\nyou now have $"+str(u.money))
                    
                    else:
                        await ctx.send("you don't have enough money for that")
                    break

    @commands.command(name='stats')
    async def stats(self, ctx):
        self.insertNewUser(ctx.author, False)
        u = self.users[ctx.author.id]
        tosend = ""
        for strain in u.weed:
            tosend += ("\n"+strain + ": " + str(u.weed[strain])+ " Gs")
        await ctx.send("**"+ctx.author.name+"**\nYou have $"+str(u.money)+tosend)

    def insertNewUser(self, user, save):
        if user.id not in self.users:
            self.users[user.id] = Rapper(uid=user.id, money=0, weed={})
            if save:
                saveUserData(self.users)

def setup(bot):
    #import ipdb;ipdb.set_trace()
    if not os.path.exists("userdata.txt"):
        saveUserData({})
    bot.add_cog(ClientCog(bot))

def parseJSON(fpath):
    with open(fpath+'.json') as json_file:
        data = json.load(json_file)
        return data

def saveUserData(users):
    #json_dict = {key: user.to_json() for key, user in users.items()}
    json_dict = {}
    for key, user in users.items():
        json_dict[key] = user.to_dict()
    with open("userdata.txt", 'w') as f:
        json.dump(json_dict, f)

#loads dict of dicts, converts to dict of rappers
def loadUserData():
    users = json.load(open('userdata.txt', 'r'))
    rappers = {}
    for key, dic in users.items():
        rappers[int(key)] = from_dict(data_class=Rapper, data=dic)
    return rappers