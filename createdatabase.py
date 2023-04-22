import json
import discord
from discord.ext import commands
TOKEN=""
intents=discord.Intents.all()
discord.member = True
intents.message_content = True
bot = discord.Client( intents=intents, case_insensitive=True)
plik = open("databaseClock.json","r")
databaseClock = json.loads(plik.read())
plik.close()
def saveClock():
    plik = open("databaseClock.json","w+")
    plik.write(json.dumps(databaseClock))
    plik.close()
@bot.event
async def on_ready():
    for guild in bot.guilds:
        for member in guild.members:
            databaseClock.append({"userId":member.id,"timeToKick":7_890_000})
            saveClock()
    print("Completed")
bot.run(TOKEN)