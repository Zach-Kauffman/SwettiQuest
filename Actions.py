import discord
from discord.ext import commands
from Rapper import Rapper
import json
import string
import os
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from dacite import from_dict
import random
from discord.ext.commands.cooldowns import BucketType

class Actions(commands.Cog):
    def __init__(self, bot):
        self.users = loadUserData()
        self.bot = bot

    @commands.command(name='asdf')
    async def asdf(self, ctx):
        tosend = discord.Embed(title="trole", description="trole", color=discord.Color.red())
        tosend.set_image(url="https://i.ya-webdesign.com/images/sad-troll-face-png-5.png")
        await ctx.send(embed=tosend)

    #rap
    #makes money based on quality of current music
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(name='rap', description='Rap to make money! The higher you are and the better your music the more money you will make')
    async def rap(self, ctx):
        self.insertNewUser(ctx.author, False)
        u = self.users[ctx.author.id]
        u.addMoney(u.moneyPerShow)
        await ctx.send(embed=makeEmbed(ctx, 'You rap really good.\ngained $' + str(u.moneyPerShow)))
        saveUserData(self.users)

    #buy N [strain]
    #buys up to N grams of selected strain
    #if N*cost>money, buys as much as possible
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(pass_context = True , aliases=['weed', 'kush', 'loud', 'dank', 'marijuana', 'cannabis', 'ganja', 'ganj'])
    async def buy(self, ctx, *args):
        strains = parseJSON("strains")
        if len(args) == 0:  
            tosend = "welcome to the weed shop. here are our strains:"
            for n in strains["strains"]:
                tosend+=("\n"+n["name"] + ": $" + str(n["price"]) + "/g")
            await ctx.send(embed=makeEmbed(ctx, tosend))
        elif len(args) >= 2:
            sname = ""
            for i in range(1, len(args)):
                sname += (args[i] + " ")
            sname = sname[:-1]
            for strain in strains["strains"]:
                if sname.upper() == strain["name"].upper():
                    self.insertNewUser(ctx.author, False)
                    u = self.users[ctx.author.id]
                    if(args[0] == "max"):
                        tobuy = u.money//int(strain["price"])
                    else:
                        tobuy = int(args[0])                           
                    if u.money >= tobuy * int(strain["price"]) and tobuy > 0:
                        u.addMoney(-tobuy * int(strain["price"]))
                        u.addWeed(str(strain["tier"]), tobuy)
                        saveUserData(self.users)
                        await ctx.send(embed=makeEmbed(ctx, "you bought "+str(tobuy)+" Gs for $" + str(tobuy*int(strain["price"]))+"\nyou now have " + str(u.weed[str(strain["tier"])]) + " Gs\nyou now have $"+str(u.money)))
                    else:
                        await ctx.send(embed=makeEmbed(ctx, "you can't afford that"))
                    break

    #smoke 1 g of your most potent weed to attempt to improve your music
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(description='hop in the stu and make some beats. improves the quality of your music so you can make more money per show. better weed = better results')
    async def produce(self, ctx):
        self.insertNewUser(ctx.author, False)
        u = self.users[ctx.author.id]
        if u.hasWeed():
            best = u.bestWeed()
            improve = random.randint(0,100)
            banger = random.randint(0,100)
            insane = random.randint(0,100)
            total = 0
            tosend = ""
            if (improve + best) >= 90:
                total += (best+1)
                tosend = ("you make a good song. +$" + str(total) + " per show")
            if (banger + best) >= 99:
                total += ((best+1)*7)
                tosend = ("that " + getNameOfStrainFromTier(best) + " hit just right and you make an absolute banger. +$" + str(total) + " per show")
            if (insane + best) >= 200:
                total += (best*best)
                tosend = ("you make one of the greatest songs of all time off that " + getNameOfStrainFromTier(best) + ". +$" + str(total) + " per show")
            u.addWeed(str(best), -1)
            if total==0:
                tosend = ("you don't make anything worthwhile")
            if(u.weed[str(best)] == 0):
                tosend += ("\nyou ran out of " + getNameOfStrainFromTier(best) + ".")
            u.improveMusic(total)
            saveUserData(self.users)   
            await ctx.send(embed=makeEmbed(ctx, tosend))
        else:
            await ctx.send(embed=makeEmbed(ctx, "you can't produce unless you have weed"))
        
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(pass_context = True , aliases=['money', 'inventory', 'cash'])
    async def stats(self, ctx):
        self.insertNewUser(ctx.author, False)
        u = self.users[ctx.author.id]
        tosend = "You have $"+str(u.money)+"\nYou make $"+str(u.moneyPerShow) + " per show"
        if u.hasWeed():
            ownedWeed = u.ownedTiersOfWeed()
            for tier in ownedWeed:
                tosend += ("\n"+getNameOfStrainFromTier(tier) + ": " + str(u.weed[tier]) + " Gs")
        else:
            tosend += "\nyou have no weed. weak."
        await ctx.send(embed=makeEmbed(ctx,tosend))

    def insertNewUser(self, user, save):
        if user.id not in self.users:
            self.users[user.id] = Rapper(uid=user.id, money=0, weed={}, moneyPerShow=1)
            if save:
                saveUserData(self.users)

def setup(bot):
    if not os.path.exists("userdata.txt"):
        saveUserData({})
    bot.add_cog(Actions(bot))

def parseJSON(fpath):
    with open(fpath+'.json') as json_file:
        data = json.load(json_file)
        return data

#returns name of strain given a specific tier
def getNameOfStrainFromTier(tier):
    strains = parseJSON("strains")['strains']
    for strain in strains:
        if str(strain['tier']) == str(tier):
            return strain['name']

#returns an embed with name bolded
#dont forget embed=makeEmbed(), not just makeEmbed() in the send()
def makeEmbed(ctx, description):
    return discord.Embed(title="**"+ctx.author.name+"**", description=description, color=colorFromID(ctx.author.id))

def colorFromID(num):
    return discord.Color(num%1000000)

def saveUserData(users):
    json_dict = {key: user.to_dict() for key, user in users.items()}
    with open("userdata.txt", 'w') as f:
        json.dump(json_dict, f)

#loads dict of dicts, converts to dict of rappers
def loadUserData():
    users = json.load(open('userdata.txt', 'r'))
    rappers = {}
    for key, dic in users.items():
        rappers[int(key)] = from_dict(data_class=Rapper, data=dic)
    return rappers