import discord
from discord.ext import commands
import time

TOKEN="Your token"
intents=discord.Intents.all()
discord.member = True
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents, case_insensitive=True)
@bot.event
async def on_ready():
    print("I'm ready!")
@bot.event
async def on_member_join(member):
    print(member.created_at.timestamp(), time.time())
    if time.time() - member.created_at.timestamp() < 7_890_000 : #3 miesiące w sekundach
        await member.kick(reason="Fresh account")
        print("git")
@bot.event
async def on_message(message):
    if message.content.lower() == "siema":
        await message.channel.send("No siema byczku :)", reference=message)
bot.run(TOKEN)