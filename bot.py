import json
import discord
from discord.ext import commands
import time
import asyncio
from discord.ext.commands import has_permissions, CheckFailure
admins_role_id=0
id_serwa=0
TOKEN=""
intents=discord.Intents.all()
discord.member = True
intents.message_content = True
bot = discord.Client( intents=intents, case_insensitive=True)
tree = discord.app_commands.CommandTree(bot)
async def check(message):
    for i in database:
        if i.get("name")==message.author.id:
            if i.get("points")>=15 and i.get("warnings")==None:
                await message.author.send("Przekroczono limit punktów karnych (1 ostrzeżenie)")
                await message.author.kick(reason="Punkty karne (1)")
                i["points"]=0
                i["warnings"]=1
                save()
            if i.get("points")>=15 and i.get("warnings")>=1:
                i["warnings"]+=1
                if i.get("warnings")<=3:
                    await message.author.send("Przekroczono limit punktów karnych ("+str(i.get("warnings"))+" ostrzeżenie)")
                    await message.author.kick(reason="Punkty karne ("+str(i.get("warnings"))+" ostrzeżeń)")
                    i["points"]=0
                elif i.get("warnings")>=4:
                    await message.author.send("Przekroczono limit punktów karnych przez co otrzymałeś bana. Skontaktuj się z administracją (RooiGevaar19#) aby zyskać możliwego unbana.")
                    await message.author.ban(reason="Punkty karne (x>=4 ostrzeżeń)")
                    i["points"]=0
                    i["warnings"]=0
                save()
def load():
    global database
    try:
        plik = open("database.json","r")
    except:
        plik = open("database.json","w")
        plik.write("[]")
        plik.close()
        database = []
        print("Restarted database! \n")
    try:
        database = json.loads(plik.read())
    except:
        plik.close()
        plik = open("database.json","a")
        plik.write("[]")
        plik.close()
        load()
    plik.close()
def save():
    plik = open("database.json","w+")
    plik.write(json.dumps(database))
    plik.close()
@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=id_serwa))
    print("I'm ready!")
@bot.event
async def on_member_join(member):
    if time.time() - member.created_at.timestamp() < 7_890_000 : #3 miesiące w sekundach
        await member.send("Twoje konto zostało uznane za skrajnie podejrzane. Spróbuj ponownie kiedy indziej :)")
        await member.kick(reason="Fresh account")
    for i in badwords:
        if i in member.display_name.lower():
            await member.send("Twój nick jest zbyt wulgarny. Zmień nick i przyjdź ponownie :)")
            await member.kick(reason="Wulgarny nick")
@bot.event
async def on_member_update(before, after):
    for i in badwords:
        if i in after.nick.lower():
            await after.edit(nick=before.nick)
            await after.send("Twój nick jest zbyt wulgarny. Został automatycznie zresetowany. Nie zmieniaj go ponownie na taki :)")      
@bot.event
async def on_message(message):
    if message.content.lower() == "siema":
        await message.channel.send("No siema :)", reference=message)
    try:
        for i in badwords:
            if i in message.content.lower():
                await message.channel.send(f"{message.author} nie ładnie tak brzydko mówić (+3 punkty karne) :(")
                await message.delete()
                czy_isnieje=False
                for i in database:
                    if i.get("name")==message.author.id:
                        i["points"]+=3
                        czy_isnieje=True
                if czy_isnieje==False:
                    database.append({"name":message.author.id,"points":0})
                save()
                await check(message)                
    except:
        pass
@tree.command(name = "clear", description = "Usuń dowolną liczbę wiadomości (uważaj bo nie ma hamulców)", guild=discord.Object(id=id_serwa)) 
@discord.app_commands.checks.has_role(admins_role_id)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.defer()
    channel = interaction.channel
    await channel.purge(limit=amount+1)
    await interaction.channel.send(f"Usunięto {amount} wiadomości, pani/panie {interaction.user}")
@clear.error
async def error_clear(interaction, x):
    await interaction.response.defer()
    channel = interaction.channel
    await channel.purge(limit=1)
    await interaction.channel.send(f"(/clear) Brak uprawnień, {interaction.user}")
load()
bot.run(TOKEN)
