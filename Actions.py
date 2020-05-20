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
import datautils
import messageutils


class Actions(commands.Cog):
    def __init__(self, bot):
        self.users = datautils.loadUserData()
        self.bot = bot

    @commands.command(name='asdf')
    async def asdf(self, ctx):
        tosend = discord.Embed(title="trole", description="trole", color=discord.Color.red())
        tosend.set_image(url="https://i.ya-webdesign.com/images/sad-troll-face-png-5.png")
        await ctx.send(embed=tosend)

    #rap
    #makes money based on quality of current music
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(pass_context = True , aliases=['r'], description='Rap to make money! The higher you are and the better your music the more money you will make')
    async def rap(self, ctx):
        datautils.insertNewUser(self.users, ctx.author, False)
        u = self.users[ctx.author.id]
        u.addMoney(u.moneyPerShow)
        await ctx.send(embed=messageutils.makeEmbed(ctx, 'You rap really good.\ngained ${:,}'.format(u.moneyPerShow)))
        datautils.saveUserData(self.users)

    #buy N [strain]
    #buys up to N grams of selected strain
    #if N*cost>money, buys as much as possible
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(pass_context = True , aliases=['weed', 'kush', 'loud', 'dank', 'marijuana', 'cannabis', 'ganja', 'ganj', 'b'])
    async def buy(self, ctx, *args):
        strains = parseJSON("strains")
        datautils.insertNewUser(self.users, ctx.author, False)
        u = self.users[ctx.author.id]
        if len(args) == 0:  
            tosend = "you have ${:,}".format(u.money)+"\nwelcome to the weed shop. here are our strains:"
            for n in strains["strains"]:
                tosend+=("\n"+n["name"] + ": ${:,}".format(n["price"]) + "/g")
            await ctx.send(embed=messageutils.makeEmbed(ctx, tosend))
        elif len(args) >= 2:
            sname = ""
            for i in range(1, len(args)):
                sname += (args[i] + " ")
            sname = sname[:-1]
            for strain in strains["strains"]:
                if sname.upper() == strain["name"].upper():
                    
                    if(args[0] == "max"):
                        tobuy = u.money//int(strain["price"])
                    else:
                        tobuy = int(args[0])                           
                    if u.money >= tobuy * int(strain["price"]) and tobuy > 0:
                        u.addMoney(-tobuy * int(strain["price"]))
                        u.addWeed(str(strain["tier"]), tobuy)
                        datautils.saveUserData(self.users)
                        await ctx.send(embed=messageutils.makeEmbed(ctx, "you bought {:,}".format(tobuy)+" Gs for ${:,}".format(tobuy*int(strain["price"]))+"\nyou now have {:,}".format(u.weed[str(strain["tier"])]) + " Gs\nyou now have ${:,}".format(u.money)))
                    else:
                        await ctx.send(embed=messageutils.makeEmbed(ctx, "you can't afford that"))
                    break

    #smoke 1 g of your most potent weed to attempt to improve your music
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(pass_context = True , aliases=['p'], description='hop in the stu and make some beats. improves the quality of your music so you can make more money per show. better weed = better results')
    async def produce(self, ctx):
        datautils.insertNewUser(self.users, ctx.author, False)
        u = self.users[ctx.author.id]
        if u.hasWeed():
            best = u.bestWeed()
            improve = random.randint(0,100)
            banger = random.randint(0,100)
            insane = random.randint(0,100)
            total = 0
            if (improve + best) >= 90:
                total += (best+1)
                tosend = ("you smoke a G of " + getNameOfStrainFromTier(best) + "\nyou make a good song. +${:,}".format(total) + " per show")
            if (banger + best) >= 99:
                total += ((best+1)*7)
                tosend = ("you smoke a G of " + getNameOfStrainFromTier(best) + "\nthat " + getNameOfStrainFromTier(best) + " hit just right and you make an absolute banger. +${:,}".format(total) + " per show")
            if (insane + best) >= 200:
                total += (best*best)
                tosend = ("you smoke a G of " + getNameOfStrainFromTier(best) + "\nyou make one of the greatest songs of all time off that " + getNameOfStrainFromTier(best) + ". +${:,}".format(total) + " per show")
            u.addWeed(str(best), -1)
            if total==0:
                tosend = ("you smoke a G of " + getNameOfStrainFromTier(best) + "\nyou don't make anything worthwhile")
            if(u.weed[str(best)] == 0):
                tosend += ("\nyou ran out of " + getNameOfStrainFromTier(best) + ".")
            u.improveMusic(total)
            datautils.saveUserData(self.users)   
            await ctx.send(embed=messageutils.makeEmbed(ctx, tosend))
        else:
            await ctx.send(embed=messageutils.makeEmbed(ctx, "you can't produce unless you have weed"))
        
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(pass_context = True, aliases=['money', 'inventory', 'cash'])
    async def stats(self, ctx):
        datautils.insertNewUser(self.users, ctx.author, False)
        u = self.users[ctx.author.id]
        tosend = "You have ${:,}".format(u.money)+"\nYou make ${:,}".format(u.moneyPerShow) + " per show"
        if u.hasWeed():
            ownedWeed = u.ownedTiersOfWeed()
            for tier in ownedWeed:
                tosend += ("\n"+getNameOfStrainFromTier(tier) + ": {:,}".format(u.weed[tier])+ " Gs")
        else:
            tosend += "\nyou have no weed. weak."
        await ctx.send(embed=messageutils.makeEmbed(ctx,tosend))

    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def leaderboard(self, ctx):
        topPlayers = []
        exclamations = ["Wow", "Spectacular", "Stupendous", "Epic", "Nice", "Awesome"]
        print(len(self.users.items()))
        for uid, player in self.users.items():
            if player not in topPlayers:
                topPlayers.append([player.name, player.money])
                if len(topPlayers) > 10:
                    minMoney = float("inf")
                    brokeBitch = 0
                    for p in topPlayers:
                        if p[1] < minMoney:
                            minMoney = p[1]
                            brokeBitch = p
                    topPlayers.remove(brokeBitch)

        tosend = "**GLOBAL LEADERBOARDS**\n"
        i = 1
        topPlayers.sort(key=lambda x:x[1], reverse=True)
        for p in topPlayers:
            #tosend += "\n" + client.fetch_user(p.uid) + ": $" + p.money
            tosend += "\n" + str(i) +": **" + p[0] + "** has ${:,}".format(p[1])
            i += 1
        tosend += "\nThere are " + str(len(self.users.items())) + " current players. **"+random.choice(exclamations)+"!**"
        await ctx.send(embed=messageutils.makeEmbed(ctx,tosend))


def setup(bot):
    if not os.path.exists(datautils.USER_DATA_PATH):
        datautils.saveUserData({})
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