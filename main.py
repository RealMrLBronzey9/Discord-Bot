import discord
import json
from discord.ext import commands
import time
import os
from dotenv import load_dotenv
from modules import remind
from BotDataJsons import wuhahaha
import asyncio

global youtubeRemindStatus 
youtubeRemindStatus = False # Status of youtube reminder function

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
        elif message.content.startswith('wuhahaha'):    # wuhahaha message as it is too long
            await message.channel.send(wuhahaha.wuhahaha1)
            await message.channel.send(wuhahaha.wuhahaha2)
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
    await ctx.channel.send('Reloaded jsons!')


# Send Message // Internals
async def sendMessage(channel_id, message):
    channel = bot.get_channel(int(channel_id))
    await channel.send(message)
    
    
# Command to remind certain ppl that a youtuber has uploaded a video
@bot.command()  
async def youtube_remind(ctx):
    api_key = os.getenv('API_KEY')
    ctx.channel.send("Youtube Reminder Started!!!")
    
    # Load the channel ID from the json file
    with open("Discord-Bot/BotDataJsons/ytremind.json") as json_file:
        data = json.load(json_file)
    
    global youtubeRemindStatus
    youtubeRemindStatus = True
    while youtubeRemindStatus:
        for i in range(len(data)):  # All users
            for j in range(len(data[str(i)]["Channels"])) :  # All channels
                channel_id = data[str(i)]["Channels"][str(j)]["id"]
                video_title, video_url, video_id = await remind.check_youtube_channel(channel_id, api_key)
                if video_title:
                    if video_id == data[str(i)]["Channels"][str(j)]["latest"]:  # Don't notification repeats
                        pass
                    else:
                        await sendMessage(1190413526888628325, f"**A new video has been uploaded!!:** {video_title}\n**Watch it here:** {video_url}")
                        data[str(i)]["Channels"][str(j)]["latest"] = video_id
                else:
                    await sendMessage(1190413526888628325, "**ERROR: Can't get video, try again.**")
            
            with open("Discord-Bot/BotDataJsons/ytremind.json", "w") as outfile:    # Save latest video id so if its same then no notification
                json.dump(data, outfile, indent=4)
        await asyncio.sleep(5)

# Stop Youtube Reminder
@bot.command()
async def youtube_remind_stop(ctx):
    global youtubeRemindStatus
    youtubeRemindStatus = False
    ctx.channel.send("Youtube Reminder Stopped!!!")
    

bot.run(TOKEN)