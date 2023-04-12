# EdaterBot.py
import os,sys,re,json
import discord
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.members = True
intents.voice_states = True
intents.messages = True
intents.guilds = True

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "ed!"

client = discord.Client(intents=intents)

helpText = f"""Commands:
• add - adds a couple eg {PREFIX} add @E-Dater1 @E-Dater2
• mute - mutes all couples
• mute - unmutes all couples
• list - lists all couples"""

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f"{PREFIX} add"):
        if message.author.guild_permissions.administrator:
            await message.channel.send(addDaters(message.content))

    if message.content.startswith(f"{PREFIX} mute"):
        daters = getDaters()
        await mute(daters, message)
        await message.channel.send("Daters Muted")

    if message.content.startswith(f"{PREFIX} unmute"):
        if message.author.guild_permissions.administrator:
            daters = getDaters()
            await unmute(daters, message)
            await message.channel.send("Daters Unmuted")

    if message.content.startswith(f"{PREFIX} help"):
        embed = discord.Embed(title= "Help", description=helpText)
        await message.channel.send(embed = embed)

    if message.content.startswith(f"{PREFIX} list"):
        await message.channel.send(embed = listCouples())

async def mute(members, message):
    for memberId in members:
        user = await message.guild.fetch_member(memberId)
        try:
            await user.edit(mute = True)
        except:
            print("not connected")

async def unmute(members, message):
    for memberId in members:
        user = await message.guild.fetch_member(memberId)
        try:
            await user.edit(mute = False)
        except:
            print("not connected")

def getDaters():
    couples = loadDatersFromFile()
    users = []

    for couple in couples:
        users.append(couple["ed1"])
        users.append(couple["ed2"])
    users = list(dict.fromkeys(users))

    return users

async def listCouples():
    couples = loadDatersFromFile()

    coupleText = ""

    for couple in couples:
        c1 = await client.get_user(couple["ed1"])
        c1 = await client.get_user(couple["ed2"])
        coupleText += f"{c1.name} + {c2.name}\n"

    embed = discord.Embed(title= "E-Daters", description=coupleText)

    return embed

def addDaters(content):
    users = {}
    parts = content.split("<")
    i = 1
    while i <= 2:
        for part in parts:
            if "@" in part:
                users[f"ed{i}"] = (re.sub("\D", "", part))
                i += 1
        break

    return saveDatersToFile(users)

def saveDatersToFile(daters):
    if len(daters) != 2:
        return "Enter two people"
    
    notExist = True

    couples = loadDatersFromFile()
    for couple in couples:
        if daters["ed1"] == couple["ed1"] and daters["ed2"] == couple["ed2"]:
            notExist = False
        else:
            continue
    
    if notExist:
        try:
            with open("daters.txt", "a") as f:
                jsonData = json.dumps(daters)
                f.write("\n"+jsonData)
        except:
            print("Error writing to file")
            print(sys.exc_info())

    if notExist:
        return "Members Added"
    elif not notExist:
        return "Members Already Added"

def loadDatersFromFile():
    couples = []
    try:
        with open("daters.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if not line == "\n":
                    couples.append(json.loads(line))

            return couples
    except:
        print("Error writing to file")
        print(sys.exc_info())

def hasPrefix(content):
    if content[:len(PREFIX)] == PREFIX:
        return True

client.run(TOKEN)
