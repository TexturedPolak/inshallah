import json
import discord
from discord.ext import commands
import time
import asyncio
from discord.ext.commands import has_permissions, CheckFailure
import datetime
import requests

# ==============================================================================================
# useful constants

HOURS = 3_600      # 1 hour in seconds
DAYS = 86_400      # 1 day in seconds

# ==============================================================================================
# bot parametres loading and checking files
try:
    file = open("config.json","r")
    config = json.loads(file.read())
    file.close()
except:
    print("Your config.json is broken, repair this and restart.")
    print("Trying to recover. Please restart.")
    URL="https://raw.githubusercontent.com/TexturedPolak/inshallah/main/sampleConfig.json"
    response = requests.get(URL)
    open("config.json", "wb").write(response.content)
    exit()
TOKEN = config.get("TOKEN")
LogsChannelId = config.get("LogsChannelId")
BanLogsChannelId = config.get("BanLogsChannelId")
KickLogsChannelId = config.get("KickLogsChannelId")
AdminRoleID = config.get("AdminRoleID")
ServerID = config.get("ServerID")
Points_BadWords = config.get("Points_BadWords")
Points_BadNick = config.get("Points_BadNick")
PointsLimit = config.get("PointsLimit")
PointsCooldownTime = config.get("PointsCooldownHoursTime") * HOURS # amount of time after which one penalty point is removed from a user 
MaxWarnings = config.get("MaxWarnings")
Account_IdleTime = config.get("Account_IdleDaysTime") * DAYS # amount of time after which the bot kicks an idle user
Account_YoungTime = config.get("Account_YoungDaysTime") * DAYS # amount of time after which the bot kicks a young account
badwords= config.get("badwords")
def checkFiles():
    emplyList = []
    time = PointsCooldownTime
    print("Checking files...")
    try:
        file = open("database.json","x")
        file.close()
        file = open("database.json","w")
        file.write(json.dumps(emplyList))
        file.close()
        print("Created database.json")
    except:
        print("database.json is already created. Pass.")
    try:
        file = open("databaseClock.json","x")
        file.close()
        file = open("databaseClock.json","w")
        file.write(json.dumps(emplyList))
        file.close()
        print("Created databaseClock.json")
    except:
        print("databaseClock.json is already created. Pass.")
    try:
        file = open("bans.json","x")
        file.close()
        file = open("bans.json","w")
        file.write(json.dumps(emplyList))
        file.close()
        print("Created bans.json")
    except:
        print("bans.json is already created. Pass.")
    try:
        file = open("time.json","x")
        file.close()
        file = open("time.json","w")
        file.write(str(time))
        file.close()
        print("Created time.json")
    except:
        print("time.json is already created. Pass.")
    print("All files checked!")
checkFiles()

# ==============================================================================================



# ==============================================================================================
# bot code


intents=discord.Intents.all()
discord.member = True
intents.message_content = True
bot = discord.Client( intents=intents, case_insensitive=True)
LogsChannel = bot.get_channel(LogsChannelId)
BanLogsChannel = bot.get_channel(BanLogsChannelId)
KickLogsChannel = bot.get_channel(KickLogsChannelId)
tree = discord.app_commands.CommandTree(bot)
plik = open("databaseClock.json","r")
databaseClock = json.loads(plik.read())
plik.close()
plik = open("database.json","r")
database = json.loads(plik.read())
plik.close()


async def check(member):
    for i in database:
        if i.get("name") == member.id:
            if i.get("points") >= PointsLimit and i.get("warnings")==None:
                await member.send("Przekroczono limit punktów karnych (1 ostrzeżenie)")
                await member.kick(reason="Punkty karne (1)")
                i["points"]=0
                i["warnings"]=1
                save()
            if i.get("points")>= PointsLimit and i.get("warnings")>=1:
                i["warnings"]+=1
                if i.get("warnings") <= MaxWarnings:
                    await member.send("Przekroczono limit punktów karnych ("+str(i.get("warnings"))+" ostrzeżenie)")
                    await member.kick(reason="Punkty karne ("+str(i.get("warnings"))+" ostrzeżeń)")
                    i["points"]=0
                    save()
                elif i.get("warnings") >= MaxWarnings+1:
                    await member.send(f"Przekroczono limit punktów karnych przez co otrzymałeś bana. Skontaktuj się z administracją, aby zyskać możliwego unbana.")
                    await member.ban(reason=f"Punkty karne (powyżej {MaxWarnings} ostrzeżeń)")
                    embed = discord.Embed(colour=discord.Colour.red(),title=f"{member} został zbanowany przez Bota")
                    embed.add_field(name="Powód:", value="Punkty Karne")
                    embed.add_field(name="ID:", value=member.id)
                    BanLogsChannel = bot.get_channel(BanLogsChannelId)
                    await BanLogsChannel.send(embed=embed)
                    i["points"]=0
                    i["warnings"]=0
                save()

async def resetPoints():
    plik = open("time.json","r")
    time = int(plik.read())
    plik.close()
    while True:
        time-=1
        save()
        await asyncio.sleep(1)
        for user in databaseClock:
            if user.get("timeToKick")<=0:
                czy_isnieje=False
                for i in database:
                    if i.get("name")==user.get("userId"):
                        i["points"]=PointsLimit
                        czy_isnieje=True
                if czy_isnieje==False:
                    database.append({"name":user.get("userId"),"points":PointsLimit})
                save()
                
                guildDoClock = bot.get_guild(ServerID)
                member = guildDoClock.get_member(user.get("userId"))
                await member.send("Zostałeś wyrzucony za bardzo małą aktywność na serwerze.")
                await check(member) 
                databaseClock.remove({"userId":user.get("userId"),"timeToKick":user.get("timeToKick")})
            else:   
                user["timeToKick"]-=1
        plik = open("databaseClock.json","w+")
        plik.write(json.dumps(databaseClock))
        plik.close()
        if time <=0:
            for i in database:
                if i.get("points")>0:
                    i["points"]-=1
            time=PointsCooldownTime

        plik = open("time.json","w+")
        plik.write(str(time))
        plik.close()

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
def addPoints(member, BadPoints):
    czy_isnieje=False
    for i in database:
        if i.get("name")==member.id:
            i["points"]+=BadPoints
            czy_isnieje=True
    if czy_isnieje==False:
        database.append({"name":member.id,"points":BadPoints})
    save()
async def checkMessage(message):
    word=""
    dlugosc = message.content
    dlugoscZbadana = 0
    for i in message.content:
        if i in [" ","!","#","%","^","*","(",")","-","+","_","=","~","`","[","]","{","}",";",":","'",'"',"|",'\\',",","<",".",">","/","?"]:
            dlugoscZbadana+=1
            if word in badwords: 
                await message.delete()
                await message.channel.send(f"{message.author.mention}, nieładnie tak brzydko mówić (+{Points_BadWords} punkty karne) :(")
                addPoints(message.author, Points_BadWords)
                await check(message.author)
               	for i in database:
                    if i.get("name")==message.author.id:
                        if i.get("warnings")==None:
                            warnings=0
                        else:
                            warnings=i.get("warnings")
                        embed = discord.Embed(
                        colour=discord.Colour.red(),
                        title=f"Twoja kartoteka obecnie:")
                        embed.add_field(name="Punkty:", value=str(i.get('points')))
                        embed.add_field(name="Ostrzeżenia:", value=str(warnings))
                        await message.channel.send(embed=embed)
            word=""
        else:
            if i == "@":
                word+="a"
            elif i=="$":
                word+="s"
            elif i=="&":
                word+="i"
            else:
                word+= i.lower()
            dlugoscZbadana+=1
        if dlugoscZbadana>=len(message.content):
            if word in badwords: 
                await message.delete()
                await message.channel.send(f"{message.author.mention}, nieładnie tak brzydko mówić (+{Points_BadWords} punkty karne) :(")
                addPoints(message.author, Points_BadWords)
                word=""
                await check(message.author)
               	for i in database:
                    if i.get("name")==message.author.id:
                        if i.get("warnings")==None:
                            warnings=0
                        else:
                            warnings=i.get("warnings")
                        embed = discord.Embed(
                        colour=discord.Colour.red(),
                        title=f"Twoja kartoteka obecnie:")
                        embed.add_field(name="Punkty:", value=str(i.get('points')))
                        embed.add_field(name="Ostrzeżenia:", value=str(warnings))
                        await message.channel.send(embed=embed)
@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=ServerID))
    print("I'm ready!")
    await resetPoints()

@bot.event
async def on_member_join(member):
    if time.time() - member.created_at.timestamp() < Account_YoungTime : 
        await member.send("Twoje konto zostało uznane za skrajnie podejrzane. Spróbuj ponownie kiedy indziej :)")
        await member.kick(reason="Fresh account")
    for i in badwords:
        if i in member.display_name.lower():
            await member.send("Twój nick jest zbyt wulgarny. Zmień nick i przyjdź ponownie :)")
            await member.kick(reason="Wulgarny nick")
    databaseClock.append({"userId":member.id,"timeToKick":Account_IdleTime})
    plik = open("databaseClock.json","w+")
    plik.write(json.dumps(databaseClock))
    plik.close()

@bot.event
async def on_member_update(before, after):
    for i in badwords:
        if i in after.nick.lower():
            await after.edit(nick=before.nick)
            await after.send(f"Twój nick jest zbyt wulgarny. Został automatycznie zresetowany. Nie zmieniaj go ponownie na taki (+{Points_BadNick} punktów karnych)")
            czy_isnieje=False
            for i in database:
                if i.get("name")==after.id:
                    i["points"]+=Points_BadNick
                    czy_isnieje=True
            if czy_isnieje==False:
                database.append({"name":after.id,"points":Points_BadNick})
            save()
            await check(after)

@bot.event
async def on_member_leave(member):
    for user in databaseClock:
        try:
            if user.get("userId") == member.id:
                databaseClock.remove({"userId":user.get("userId"),"timeToKick":user.get("timeToKick")})
        except:
            pass

@bot.event
async def on_member_remove(member):
    guild = member.guild
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
        if entry.target == member:
            embed = discord.Embed(colour=discord.Colour.red(),title=f"{member} został wyrzucony przez {entry.user}")
            embed.add_field(name="Powód:", value=entry.reason)
            embed.add_field(name="ID:", value=member.id)
            KickLogsChannel = bot.get_channel(KickLogsChannelId)
            await KickLogsChannel.send(embed=embed)
    for user in databaseClock:
        try:
            if user.get("userId") == member.id:
                databaseClock.remove({"userId":user.get("userId"),"timeToKick":user.get("timeToKick")})
        except:
            pass
@bot.event
async def on_member_ban(guild, member):
    plik = open("bans.json","r")
    bans = json.loads(plik.read())
    plik.close()
    banned_reason=None
    async for entry in guild.bans(limit=10):
        if entry.user.id == member.id:
            banned_reason=entry.reason
    bans.append({"dateBan":str(datetime.datetime.now()),"id":str(member.id),"reason":str(banned_reason),"caughtNick":str(member),"accCreated":str(member.created_at.astimezone()),"joinServer":str(member.joined_at.astimezone())})
    plik = open("bans.json","w+")
    plik.write(json.dumps(bans))
    plik.close()
    for user in databaseClock:
        try:
            if user.get("userId") == member.id:
                databaseClock.remove({"userId":user.get("userId"),"timeToKick":user.get("timeToKick")})
        except:
            pass
    guild = member.guild
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
        if entry.target == member:
            embed = discord.Embed(colour=discord.Colour.red(),title=f"{member} został zbanowany przez {entry.user}")
            embed.add_field(name="Powód:", value=entry.reason)
            embed.add_field(name="ID:", value=member.id)
            BanLogsChannel = bot.get_channel(BanLogsChannelId)
            await BanLogsChannel.send(embed=embed)
    for user in databaseClock:
        try:
            if user.get("userId") == member.id:
                databaseClock.remove({"userId":user.get("userId"),"timeToKick":user.get("timeToKick")})
        except:
            pass
@bot.event
async def on_message(message):
    for i in databaseClock:
        if message.author.id == i.get("userId"):
                i["timeToKick"] = Account_IdleTime
    if message.content.lower() == "siema":
        await message.channel.send("No siema :)", reference=message)
    await checkMessage(message)
		    
@bot.event
async def on_message_edit(before, after):
    await checkMessage(after)

@tree.command(name = "clear", description = "Usuń dowolną liczbę wiadomości (uważaj, bo nie ma hamulców)", guild=discord.Object(id=ServerID)) 
@discord.app_commands.checks.has_role(AdminRoleID)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.defer()
    channel = interaction.channel
    await channel.purge(limit=amount+1)
    await interaction.channel.send(f"Usunięto {amount} wiadomości, pani/panie {interaction.user.mention}")

@clear.error
async def error_clear(interaction, x):
    await interaction.response.send_message(f"(/clear) Brak uprawnień, {interaction.user.mention}")

@tree.command(name = "kartoteka", description = "Sprawdź swoją kartotekę", guild=discord.Object(id=ServerID)) 
async def kartoteka(interaction: discord.Interaction):
    wykrocz=False
    for i in database:
        if i.get("name")==interaction.user.id:
            if i.get("warnings")==None:
                warnings=0
            else:
                warnings=i.get("warnings")
            embed = discord.Embed(
            colour=discord.Colour.red(),
            title=f"Twoja kartoteka {interaction.user.name}:")
            embed.add_field(name="Punkty:", value=str(i.get('points')))
            embed.add_field(name="Ostrzeżenia:", value=str(warnings))
            embed.add_field(name="Przypominamy", value=f"Za każde {PointsLimit} punktów otrzymujesz ostrzeżenie i zostajesz wyrzucony z serwera (twoje punkty się zerują także przy tym). Każdy otrzymuje maksymalnie {MaxWarnings} otrzeżenia. Gdy po raz {MaxWarnings+1}. uzbiera ci się {PointsLimit} punktów, zostajesz zbanowany i pozostaje ci się odwołać u moderatora czy admina.", inline=False)
            await interaction.response.send_message(embed=embed)
            wykrocz=True
    if wykrocz==False:
        await interaction.response.send_message(f"{interaction.user.mention}, nie posiadasz żadnych wykroczeń i nie byłeś nigdy notowany.")

@tree.command(name = "księga-wykroczeń", description = "Sprawdź czyjąś bibliotekę", guild=discord.Object(id=ServerID)) 
@discord.app_commands.checks.has_role(AdminRoleID)
async def ksiega(interaction: discord.Interaction, uzytkownik: discord.Member):
    wykrocz=False
    for i in database:
        if i.get("name")==uzytkownik.id:
            if i.get("warnings")==None:
                warnings=0
            else:
                warnings=i.get("warnings")
            embed = discord.Embed(
            colour=discord.Colour.red(),
            title=f"Kartoteka użytkonika {uzytkownik.name}:")
            embed.add_field(name="Punkty:", value=str(i.get('points')))
            embed.add_field(name="Ostrzeżenia:", value=str(warnings))
            embed.add_field(name="Przypominamy", value=f"Za każde {PointsLimit} punktów otrzymujesz ostrzeżenie i zostajesz wyrzucony z serwera (twoje punkty się zerują także przy tym). Każdy otrzymuje maksymalnie {MaxWarnings} otrzeżenia. Gdy po raz {MaxWarnings+1}. uzbiera ci się {PointsLimit} punktów, zostajesz zbanowany i pozostaje ci się odwołać u moderatora czy admina.", inline=False)
            await interaction.response.send_message(embed=embed)
            wykrocz=True
    if wykrocz==False:
        await interaction.response.send_message(f"{uzytkownik.mention}, nie posiada żadnych wykroczeń i nie był nigdy notowany.")

@ksiega.error
async def error_ksiega(interaction, x):
    channel = interaction.channel
    await interaction.response.send_message(f"(/księga-wykroczeń) Brak uprawnień, {interaction.user.mention}")


@tree.command(name = "mandat", description = "Ukaraj kogoś paroma punktami", guild=discord.Object(id=ServerID)) 
@discord.app_commands.checks.has_role(AdminRoleID)
async def mandat(interaction: discord.Interaction, uzytkownik: discord.Member, ilosc: int, powod: str):
    addPoints(uzytkownik, ilosc)
    await check(uzytkownik)
    embed = discord.Embed(colour=discord.Colour.red(),title=f"Zostałeś ukarany {uzytkownik}!")
    embed.add_field(name="Powód:", value=powod)
    embed.add_field(name="Ilość punktów", value=str(ilosc))
    for i in database:
        if i.get("name")==uzytkownik.id:
            embed2 = discord.Embed(colour=discord.Colour.red(),title=f"Twoja kartoteka obecnie:")
            embed2.add_field(name="Punkty:", value=str(i.get('points')))
            if i.get("warnings")==None:
                warnings=0
            else:
                warnings=i.get("warnings")
            embed2.add_field(name="Ostrzeżenia:", value=str(warnings))
    LogsChannel = bot.get_channel(LogsChannelId)
    await LogsChannel.send(embed=embed)
    await interaction.channel.send(embed=embed2)
    await interaction.response.send_message(embed=embed)
@mandat.error
async def error_mandat(interaction, x):
    await interaction.response.send_message(f"(/mandat) Brak uprawnień, {interaction.user.mention}")
@tree.command(name = "daruj-kare", description = "Usun parę punktów z czyjegoś konta", guild=discord.Object(id=ServerID)) 
@discord.app_commands.checks.has_role(AdminRoleID)
async def darujKare(interaction: discord.Interaction, uzytkownik: discord.Member, ilosc: int):
    czy_isnieje = False
    for i in database:
        if uzytkownik.id == i.get("name"):
            if i.get("points") <= ilosc:
                i["points"]=0
            else:
                i["points"]-=ilosc
            save()
            await check(uzytkownik)
            LogsChannel = bot.get_channel(LogsChannelId)
            await LogsChannel.send(f"{interaction.user.mention},odjęto punkty użytkownikowi {uzytkownik.mention}. Liczba odjętych punktów: {ilosc}.")
            await interaction.response.send_message(f"{interaction.user.mention},odjęto punkty użytkownikowi {uzytkownik.mention}. Liczba odjętych punktów: {ilosc}.")
            czy_isnieje = True
    if czy_isnieje == False:
            await interaction.response.send_message("Brak użytkownika w bazie danych.")
@darujKare.error
async def error_darujKare(interaction, x):
    await interaction.response.send_message(f"(/daruj-kare) Brak uprawnień, {interaction.user.mention}")
@tree.command(name = "pal-gume", description = "Do kickowania użytkowników", guild=discord.Object(id=ServerID)) 
@discord.app_commands.checks.has_role(AdminRoleID)
async def palGume(interaction: discord.Interaction, uzytkownik: discord.Member, powod: str):
    await uzytkownik.send(f'Zostałeś wyrzucony z powodu: "{powod}" przez {interaction.user.mention}')
    await uzytkownik.kick(reason=powod)
    embed = discord.Embed(colour=discord.Colour.yellow(),title=f"{uzytkownik} został wyrzucony przez {interaction.user}")
    embed.add_field(name="Powód:", value=powod)
    embed.add_field(name="ID:", value=uzytkownik.id)
    embed2 = discord.Embed(colour=discord.Colour.red(),title=f"{interaction.user} użył komendy /pal-gume")
    KickLogsChannel = bot.get_channel(KickLogsChannelId)
    await KickLogsChannel.send(embed=embed2)
    await interaction.response.send_message(embed=embed)
@palGume.error
async def error_palGume(interaction, x):
    await interaction.response.send_message(f"(/pal-gume) Brak uprawnień, {interaction.user.mention}")
@tree.command(name = "won", description = "Do banowania użytkowników", guild=discord.Object(id=ServerID)) 
@discord.app_commands.checks.has_role(AdminRoleID)
async def won(interaction: discord.Interaction, uzytkownik: discord.Member, powod: str):
    await uzytkownik.ban(reason=powod)
    embed = discord.Embed(colour=discord.Colour.red(),title=f"{uzytkownik} został zbanowany przez {interaction.user}")
    embed.add_field(name="Powód:", value=powod)
    embed.add_field(name="ID:", value=uzytkownik.id)
    BanLogsChannel = bot.get_channel(BanLogsChannelId)
    embed2 = discord.Embed(colour=discord.Colour.yellow(),title=f"{interaction.user} użył komendy /won")
    await BanLogsChannel.send(embed=embed2)
    await interaction.response.send_message(embed=embed)

@won.error
async def error_won(interaction, x):
    await interaction.response.send_message(f"(/won) Brak uprawnień, {interaction.user.mention}")
load()
bot.run(TOKEN)
