import discord
import json
from discord.ext import commands
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='%', intents=intents)
intents.message_content = True
intents.members = True
intents.guilds = True


# Json Datas
def load_json(file):
    with open(file) as file_json:
        file_data = file_json.read()
    file_content = json.loads(file_data)
    return file_content

message_replies = load_json("Discord-Bot/BotDataJsons/messagereplies.json")

    
# On Ready
@bot.event
async def on_ready():
    print(f'{bot.user} has logged into discord!!')
    
    

### Bot Functionality

## Events
# Message Replies
@bot.event 
async def on_message(message):
    if message.author == bot.user:
        return
    for i in message_replies:
        if message.content.startswith(i):
            await message.channel.send(message_replies[i])
            break
    await bot.process_commands(message) # If the message is a command
    

# Detect if someone left voicecall
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel and not after.channel:
        await sendMessage(1121293805228916768, f'{member} left {before.channel}!')
        context = None
        if len(before.channel.members) == 0:
            await sendMessage(1121293805228916768, f'***!! The call on {before.channel} ended on {time.ctime()} !! \n ---------------------------------------***')
    elif before.channel == None and after.channel != None:
        await sendMessage(1121293805228916768, f'{member} joined {after.channel}!')


## Commands
# Reload Json Files
@bot.command()
async def reloadjson(ctx):
    global message_replies
    global banned_members
    message_replies = load_json("Discord-Bot/BotDataJsons/messagereplies.json")
    banned_members = load_json("Discord-Bot/BotDataJsons/bannedmembers.json")
    await ctx.channel.send('Reloaded jsons!')

# Send Message // Internals
async def sendMessage(channel_id, message):
    channel = bot.get_channel(int(channel_id))
    await channel.send(message)


bot.run(TOKEN)