import discord
import json
from discord.ext import commands
import time

# Set up
with open("BotDataJsons\\token.json") as token_json:
    token_data = token_json.read()
token_data2 = json.loads(token_data)

TOKEN = str(token_data2['DISCORD_TOKEN'])
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

message_replies = load_json("BotDataJsons\messagereplies.json")
banned_members = load_json("BotDataJsons\\bannedmembers.json")

    
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

# Member Filtering
@bot.event
async def on_member_join(member):
    for i in banned_members:
        if member.id == banned_members[i]:
            await member.kick()
            print(f'Kicked, {str(member.id)} also known as {member}')
            break
    join_channel = bot.get_channel(1117997142334775369)
    await join_channel.send(f'{member} has joined!!')
    

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
    message_replies = load_json("BotDataJsons\messagereplies.json")
    banned_members = load_json("BotDataJsons\\bannedmembers.json")
    await ctx.channel.send('Reloaded jsons!')

# Append Banned Member
@bot.command()
async def blacklist(ctx, membername, memberid):
    banned_members[membername] = int(memberid)
    with open("DiscordBot\BotData\\bannedmembers.json", 'w') as file:
        json.dump(banned_members, file)
    await ctx.channel.send(f'Blacklisted {membername} also known as {memberid} from joining!')


# Send Message // Internals
async def sendMessage(channel_id, message):
    channel = bot.get_channel(int(channel_id))
    await channel.send(message)


bot.run(TOKEN)