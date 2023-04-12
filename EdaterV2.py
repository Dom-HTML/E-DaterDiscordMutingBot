# EdaterV2.py
import os,sys,re,json
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.members = True
intents.voice_states = True
intents.messages = True
intents.guilds = True
intents.message_content = True

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "ed!"

bot = commands.Bot(command_prefix=PREFIX ,intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is Online')

@bot.command(name="add",
                description="adds a couple",
                brief="add",
                aliases=["ad"],
                pass_context=True)
@commands.has_role("Dom")
async def addCouple(ctx, e1, e2):
    daters = {"e1":re.sub("\D", "", e1), "e2":re.sub("\D", "", e2)}
    saveDatersToFile(daters)

    embed = discord.Embed(title="Couple Added")
    await ctx.send(embed=embed)

@bot.command(name="mute",
                description="Mutes Couples",
                brief="mute",
                aliases=["mut"],
                pass_context=True)
@commands.has_role("Non E-daters")
async def mute(ctx):
    couples = loadDatersFromFile()
    for couple in couples:
        e1Member = await getMember(ctx, couple["e1"])
        e2Member = await getMember(ctx, couple["e2"])
        print(e1Member.voice)
        print(e2Member.voice)
        if e1Member.voice and e2Member.voice:
            if e1Member.voice.channel == e2Member.voice.channel:
                print("Muted Them E-daters")
                await e1Member.edit(mute = True)
                await e2Member.edit(mute = True)
            
                embed = discord.Embed(title="Couple Muted",
                                  description=f"{e1Member.name}+{e2Member.name}")
                await ctx.send(embed=embed)

@bot.command(name="unmute",
                description="Unmutes Couples",
                brief="unmute",
                aliases=["unmut"],
                pass_context=True)
@commands.has_role("Non E-daters")
async def unmute(ctx):
    couples = loadDatersFromFile()
    for couple in couples:
        e1Member = await getMember(ctx, couple["e1"])
        e2Member = await getMember(ctx, couple["e2"])
        print(e1Member.voice)
        print(e2Member.voice)
        await e1Member.edit(mute = False)
        await e2Member.edit(mute = False)

        embed = discord.Embed(title="Couple Unmuted",
                                  description=f"{e1Member.name}+{e2Member.name}")
        await ctx.send(embed=embed)

def saveDatersToFile(daters):
    try:
        with open("daters.txt", "a") as f:
            jsonData = json.dumps(daters)
            f.write("\n"+jsonData)
    except:
        print("Error writing to file")
        print(sys.exc_info())

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

async def getMember(ctx, mid):
    guild = ctx.guild
    member = await guild.fetch_member(mid)
    return member

bot.run(TOKEN)


