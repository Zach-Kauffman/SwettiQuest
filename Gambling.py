import datautils
import discord
from discord.ext import commands
import random
import os
from Rapper import Rapper
from discord.ext.commands.cooldowns import BucketType
import messageutils

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.users = datautils.loadUserData()
        self.bot = bot

    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(name='coinflip')
    async def coinflip(self, ctx, *args):
        datautils.insertNewUser(self.users, ctx.author, False)
        u = self.users[ctx.author.id]
        if (str(args[0])[0].upper() == 'H' or str(args[0])[0].upper() == 'T'):
            canAfford = True
            if args[1] == 'max':
                bet = u.money
            elif u.money < int(args[1]):
                tosend = "you don't have enough money" 
                canAfford = False
            else:
                bet = int(args[1])
            if canAfford:
                coin = random.randint(0,1)
                response = ["heads", "tails"]
                tosend = "you bet $"+str(bet)+"\ncoin landed on " + response[coin]
                if (str(args[0])[0].upper() == 'H' and coin == 0) or (str(args[0])[0].upper() == 'T' and coin == 1):
                    u.addMoney(bet)
                    tosend += "\n**you won $" + str(bet) + "**"
                else:
                    u.addMoney(-1*bet)
                    tosend+="\nyou lost... heh..."
        else:
            tosend = "use $coinflip [h/t] [bet] ya fuckin dingus"
        datautils.saveUserData(self.users)
        await ctx.send(embed=messageutils.makeEmbed(ctx, tosend))

def setup(bot):
    if not os.path.exists(datautils.USER_DATA_PATH):
        datautils.saveUserData({})
    bot.add_cog(Gambling(bot))