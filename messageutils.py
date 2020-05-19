import discord

#returns an embed with name bolded
#dont forget embed=makeEmbed(), not just makeEmbed() in the send()
def makeEmbed(ctx, description):
    return discord.Embed(title="**"+ctx.author.name+"**", description=description, color=colorFromID(ctx.author.id))

def colorFromID(num):
    return discord.Color(num%1000000)