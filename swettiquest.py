import discord
import pickle
from User import User
import random
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()
users = {}

@client.event
async def on_ready():
    print('SwettiQuest running on {0.user}'.format(client))
    if(os.path.exists("userdata.txt")):
        print('Loading user data...')
        global users
        users = loadUserData()
        print('Loaded data for ' + str(len(users)) + ' users')
        print(users)

@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.content.startswith('$'):
        u = User(message.author.id)
        global users
        print(users)
        if u.id not in users:
            print("user not found")
            users[u.id] = u
        else:
            print("user found")

        saveUserData()
    
    return

def saveUserData():
    global users
    pickle.dump(users, open('userdata.txt', 'wb'))

def loadUserData():
    return pickle.load(open('userdata.txt', 'rb'))

client.run(token)