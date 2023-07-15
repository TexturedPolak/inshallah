import json
import discord
from discord.ext import commands
import time
import asyncio
from discord.ext.commands import has_permissions, CheckFailure
import datetime
import requests
from cryptography.fernet import Fernet
import base64
import psycopg2
import random
import string
from captcha.image import ImageCaptcha
import os
import math
from craiyon import Craiyon, craiyon_utils
from io import BytesIO
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#import tempfile
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
DoAutomodMessages = config.get("DoAutomodMessages")
BumpChannelID= config.get("BumpChannelID")
PhothosChannels=config.get("PhothosChannels")
databaseName=config.get("databaseName")
databaseHost=config.get("databaseHost")
databasePort=config.get("databasePort")
databaseUser=config.get("databaseUser")
databasePassword=config.get("databasePassword")
VerificationRoleId=config.get("VerificationRoleId")
channelLogiWeryfikacja=config.get("channelLogiWeryfikacja")
verificationCategory=config.get("verificationCategory")
levelsChannel=config.get("levelsChannel")
welcomeChannel=config.get("welcomeChannel")
byeChannel=config.get("byeChannel")
BackupFolderGDID = config.get("BackupFolderGDID")
mydb = psycopg2.connect(
  database=databaseName,  
  host=databaseHost,
  port=databasePort,
  user=databaseUser,
  password=databasePassword
)
mycursor = mydb.cursor()

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
def leveleNapraw():
    sql= "SELECT * FROM levele"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    for result in results:
        level=int(math.sqrt(result[1]/10))
        sql = "UPDATE levele SET level = %s WHERE discordid=%s"
        val=[level,result[0]]
        mycursor.execute(sql,val)
        mydb.commit()
async def dajLevele(userID, beforeLevel):
    sql= "SELECT xp FROM levele WHERE discordid=%s"
    val =[(userID)]
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    level=int(math.sqrt(result[0][0]/10))
    sql = "UPDATE levele SET level = %s WHERE discordid=%s"
    val=[level,userID]
    mycursor.execute(sql,val)
    mydb.commit()
    if level>beforeLevel:
        channel = discord.utils.get(bot.get_all_channels(), id=levelsChannel)
        user = bot.get_user(int(userID))
        embed = discord.Embed(colour=discord.Colour.green(),title=f"{user.display_name} zdobył(a) {level} poziom! Gratulujemy :grin:")
        await channel.send(embed=embed)
async def dodajXP(ilosc,userID):
    global mycursor
    global mydb
    sql= "SELECT * FROM levele WHERE discordid=%s"
    val =(userID,)
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    #except:
     #   print("Restart")
      #  await bot.change_presence(status=discord.Status.online, activity=discord.Game('Restartowanie!'))
       # os._exit(1)

    user = bot.get_user(int(userID))
    if result == [] and user.bot == False:
        beforeLevel=0
        sql = "INSERT INTO levele VALUES (%s,%s,%s)"
        val = [userID,ilosc,0]
        mycursor.execute(sql, val)
        mydb.commit()
    elif user.bot == False:
        beforeLevel=result[0][2]
        sql = "UPDATE levele SET xp = xp+%s WHERE discordid=%s"
        val=[ilosc,userID]
        mycursor.execute(sql,val)
        mydb.commit()
    if user.bot==False:
        await dajLevele(userID,beforeLevel)

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
            print("Restart")
            await bot.change_presence(status=discord.Status.online, activity=discord.Game('Restartowanie!'))
            os._exit(1)
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
            
            sql="SELECT word FROM badwords WHERE word=%s"
            val=[(word)]
            mycursor.execute(sql,val)
            badword = mycursor.fetchall()

            if word == badword: 
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
            sql="SELECT word FROM badwords WHERE word=%s"
            val=[(word)]
            mycursor.execute(sql,val)
            badword = mycursor.fetchall()

            if badword==[]:
                czyTak=False
            else:
                czyTak=True

            if czyTak: 
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
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Miłego dnia :)'))
    print("I'm ready!")
    await resetPoints()

@bot.event
async def on_member_join(member):
    if time.time() - member.created_at.timestamp() < Account_YoungTime : 
        try:
            await member.send("Twoje konto zostało uznane za skrajnie podejrzane. Spróbuj ponownie kiedy indziej :)")
        except:
            pass
        await member.kick(reason="Nowe konto")
    for i in badwords:
        if i in member.display_name.lower():
            await member.send("Twój nick jest zbyt wulgarny. Zmień nick i przyjdź ponownie :)")
            await member.kick(reason="Wulgarny nick")
    databaseClock.append({"userId":member.id,"timeToKick":Account_IdleTime})
    plik = open("databaseClock.json","w+")
    plik.write(json.dumps(databaseClock))
    plik.close()

    # ------- Verification Module --------
    guild = bot.get_guild(ServerID)
    admin_role = guild.get_role(AdminRoleID)
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True)
    }
    nameChannel=""
    nameChannel+="Weryfikacja-"
    nameChannel+=str(member)
    category = discord.utils.get(guild.categories, id=verificationCategory)
    channel = await guild.create_text_channel(nameChannel, overwrites=overwrites, category=category)
    embed = discord.Embed(colour=discord.Colour.blue(),title=f"Weryfikacja",description="Chcemy mieć czystą i bezpieczną społeczność. Osoby, które mają świeżo założone konta, będą automatycznie wyrzucane przez bota z serwera. Czas na przejście weryfikacji to 15 minut.\nProsimy Ciebie abyś odpowiedział(a) na 5 pytań. Przed rozpoczęciem prosimy Cię o dokładne przeczytanie regulaminu. **Proces weryfikacji może być przerywany paru sekundowymi przerwami (max 5 sekund), w oczekiwaniu na wygenerowanie pytania.**")
    await channel.send(f"{member.mention}")
    await channel.send(embed=embed)
    async def verificationWaiting():
        nonlocal stopZegar
        verificationTime=900
        userData=[member,channel,verificationTime]
        while userData[2]>0:
            userData[2]=userData[2]-1
            await asyncio.sleep(1)
            if stopZegar:
                break
        if stopZegar==False:
            await userData[1].delete()
            try:    
                await userData[0].send("Czas na weryfikację minął!")
            except:
                pass
            await userData[0].kick(reason="Czas na weryfikację minął!")
            await sendLogiWeryfikacja()
        return None
    stopZegar=False
    loop = asyncio.get_event_loop()
    loop.create_task(verificationWaiting())
    logiWeryfikacja=""
    async def sendLogiWeryfikacja():
        if logiWeryfikacja[-8:]=="udana!**":
            kolor=discord.Colour.green()
        else:
            kolor=discord.Colour.red()
        embed = discord.Embed(colour=kolor,title=f"Weryfikacja użytkownika {member}, ID: {member.id}",description=logiWeryfikacja)
        logsChannel = discord.utils.get(bot.get_all_channels(), id=channelLogiWeryfikacja)
        await logsChannel.send(embed=embed)
    # Pytanie 6
    async def pytanieSzesc():
        class Pytanie(discord.ui.View):
            @discord.ui.button(label="TAK", row=0, style=discord.ButtonStyle.primary)
            async def first_button(self, button, interaction):
                nonlocal stopZegar
                nonlocal logiWeryfikacja
                logiWeryfikacja+="**Pytanie 6**\nJesteś osobą która szanuje osoby z tęczowego środowiska?\nOdpowiedź: `TAK`\n\n**Weryfikacja udana!**"
                await sendLogiWeryfikacja()
                await channel.delete()
                try:
                    await member.send("Weryfikacja zakończona sukcesem!")
                except:
                    pass
                role = discord.utils.get(channel.guild.roles, id=VerificationRoleId)
                await member.add_roles(role)
                stopZegar=True
                await asyncio.sleep(2)
            @discord.ui.button(label="NIE", row=0, style=discord.ButtonStyle.primary)
            async def second_button(self, button, interaction):
                nonlocal stopZegar
                nonlocal logiWeryfikacja
                logiWeryfikacja+="**Pytanie 6**\nJesteś osobą która szanuje osoby z tęczowego środowiska?\nOdpowiedź: `NIE`\n\n**Weryfikacja nieudana!**"
                await sendLogiWeryfikacja()
                await channel.delete()
                try:
                    await member.send("Na serwer wpuszczamy osoby tolerancyjne i szanujące każdego, nawet te z tęczowego środowiska.")
                except:
                    pass
                await member.ban(reason="Osoba anty LGBTQ+")
                stopZegar=True
        embed = discord.Embed(colour=discord.Colour.blue(),title=f"Pytanie 6",description="Jesteś osobą która szanuje osoby z tęczowego środowiska?")
        await channel.send(embed=embed,view=Pytanie())
    # Pytanie 5
    async def pytaniePiec(ostatnie,ostatniejsze):
        sql="SELECT pytanie,a,b,c,poprawna FROM pytania WHERE id=%s"
        value=random.randint(1, 16)
        val=[(value)]
        mycursor.execute(sql,val)
        pytanie = mycursor.fetchall()
        poprawna=pytanie[0][4]
        if value == ostatnie or value==ostatniejsze:
            sql="SELECT pytanie,a,b,c,poprawna FROM pytania WHERE id=%s"
            value=random.randint(1, 16)
            val=[(value)]
            mycursor.execute(sql,val)
            pytanie = mycursor.fetchall()
            poprawna=pytanie[0][4]
        async def sprOdp(odp):
            nonlocal stopZegar
            nonlocal logiWeryfikacja
            if odp==poprawna:
                logiWeryfikacja+="**Pytanie 5**\n"+pytanie[0][0]+"\nOdpowiedź: `"+odp+"`\nOdpowiedziano poprawnie.\n\n**Weryfikacja udana!**"
                await sendLogiWeryfikacja()
                await channel.delete()
                try:
                    await member.send("Weryfikacja zakończona sukcesem!")
                except:
                    pass
                role = discord.utils.get(channel.guild.roles, id=VerificationRoleId)
                await member.add_roles(role)
                welChannel = discord.utils.get(bot.get_all_channels(), id=welcomeChannel)
                await welChannel.send(f"Osoba o nicku {member.mention}, właśnie prześlizgnęła się na nasz serwer. Witamy :wave::partying_face:")
                stopZegar=True
            else:
                logiWeryfikacja+="**Pytanie 5**\n"+pytanie[0][0]+"\nOdpowiedź: `"+odp+"`\nPoprawna odpowiedź: "+poprawna+"\n\n**Weryfikacja nieudana!**"
                await sendLogiWeryfikacja()
                await channel.delete()
                try:
                    await member.send("Odpowiedziałeś niepoprawnie na pytanie z regulaminu. Spróbuj ponownie.")
                except:
                    pass
                await member.kick(reason="Pytanie z regulaminu. Niepoprawna weryfikcja.")
                stopZegar=True      
        class Pytanie(discord.ui.View):
            @discord.ui.button(label="A", row=0, style=discord.ButtonStyle.primary)
            async def first_button(self, button, interaction):
                odp="a"
                await sprOdp(odp)
            @discord.ui.button(label="B", row=0, style=discord.ButtonStyle.primary)
            async def second_button(self, button, interaction):
                odp="b"
                await sprOdp(odp)
            @discord.ui.button(label="C", row=0, style=discord.ButtonStyle.primary)
            async def third_button(self, button, interaction):
                odp="c"
                await sprOdp(odp)
        embed = discord.Embed(colour=discord.Colour.blue(),title=f"Pytanie 5",description="**"+pytanie[0][0]+"**\na) "+pytanie[0][1]+"\nb) "+pytanie[0][2]+"\nc) "+pytanie[0][3])
        await channel.send(embed=embed,view=Pytanie())
    # Pytanie 4
    async def pytanieCztery(ostatnie):
        sql="SELECT pytanie,a,b,c,poprawna FROM pytania WHERE id=%s"
        value=random.randint(1, 16)
        val=[(value)]
        mycursor.execute(sql,val)
        pytanie = mycursor.fetchall()
        poprawna=pytanie[0][4]
        if value == ostatnie:
            sql="SELECT pytanie,a,b,c,poprawna FROM pytania WHERE id=%s"
            value=random.randint(1, 16)
            val=[(value)]
            mycursor.execute(sql,val)
            pytanie = mycursor.fetchall()
            poprawna=pytanie[0][4]
        async def sprOdp(odp):
            nonlocal stopZegar
            nonlocal logiWeryfikacja
            if odp==poprawna:
                logiWeryfikacja+="**Pytanie 4**\n"+pytanie[0][0]+"\nOdpowiedź: `"+odp+"`\nOdpowiedziano poprawnie.\n\n"
                await channel.purge(limit=3)
                await pytaniePiec(value,ostatnie)
            else:
                logiWeryfikacja+="**Pytanie 4**\n"+pytanie[0][0]+"\nOdpowiedź: `"+odp+"`\nPoprawna odpowiedź: "+poprawna+"\n\n**Weryfikacja nieudana!**"
                await sendLogiWeryfikacja()
                await channel.delete()
                try:
                    await member.send("Odpowiedziałeś niepoprawnie na pytanie z regulaminu. Spróbuj ponownie.")
                except:
                    pass
                await member.kick(reason="Pytanie z regulaminu. Niepoprawna weryfikcja.")
                stopZegar=True
        class Pytanie(discord.ui.View):
            @discord.ui.button(label="A", row=0, style=discord.ButtonStyle.primary)
            async def first_button(self, button, interaction):
                odp="a"
                await sprOdp(odp)
            @discord.ui.button(label="B", row=0, style=discord.ButtonStyle.primary)
            async def second_button(self, button, interaction):
                odp="b"
                await sprOdp(odp)
            @discord.ui.button(label="C", row=0, style=discord.ButtonStyle.primary)
            async def third_button(self, button, interaction):
                odp="c"
                await sprOdp(odp)
        embed = discord.Embed(colour=discord.Colour.blue(),title=f"Pytanie 4",description="**"+pytanie[0][0]+"**\na) "+pytanie[0][1]+"\nb) "+pytanie[0][2]+"\nc) "+pytanie[0][3])
        await channel.send(embed=embed,view=Pytanie())
    # Pytanie 3
    async def pytanieTrzy():
        sql="SELECT pytanie,a,b,c,poprawna FROM pytania WHERE id=%s"
        value=random.randint(1, 16)
        val=[(value)]
        mycursor.execute(sql,val)
        pytanie = mycursor.fetchall()
        poprawna=pytanie[0][4]
        async def sprOdp(odp):
            nonlocal stopZegar
            nonlocal logiWeryfikacja
            if odp==poprawna:
                logiWeryfikacja+="**Pytanie 3**\n"+pytanie[0][0]+"\nOdpowiedź: `"+odp+"`\nOdpowiedziano poprawnie.\n\n"
                await channel.purge(limit=3)
                await pytanieCztery(value)
            else:
                logiWeryfikacja+="**Pytanie 3**\n"+pytanie[0][0]+"\nOdpowiedź: `"+odp+"`\nPoprawna odpowiedź: "+poprawna+"\n\n**Weryfikacja nieudana!**"
                await sendLogiWeryfikacja()
                await channel.delete()
                try:
                    await member.send("Odpowiedziałeś niepoprawnie na pytanie z regulaminu. Spróbuj ponownie.")
                except:
                    pass
                await member.kick(reason="Pytanie z regulaminu. Niepoprawna weryfikcja.")
                stopZegar=True
        class Pytanie(discord.ui.View):
            @discord.ui.button(label="A", row=0, style=discord.ButtonStyle.primary)
            async def first_button(self, button, interaction):
                odp="a"
                await sprOdp(odp)
            @discord.ui.button(label="B", row=0, style=discord.ButtonStyle.primary)
            async def second_button(self, button, interaction):
                odp="b"
                await sprOdp(odp)
            @discord.ui.button(label="C", row=0, style=discord.ButtonStyle.primary)
            async def third_button(self, button, interaction):
                odp="c"
                await sprOdp(odp)
        embed = discord.Embed(colour=discord.Colour.blue(),title=f"Pytanie 3",description="**"+pytanie[0][0]+"**\na) "+pytanie[0][1]+"\nb) "+pytanie[0][2]+"\nc) "+pytanie[0][3])
        await channel.send(embed=embed,view=Pytanie())
    
    
    
    # Pytanie 2
    async def pytanieDwa(usun):
        nonlocal logiWeryfikacja
        liczba1 = random.randint(1, 10)
        liczba2 = random.randint(1, 10)
        wynik = liczba1 * liczba2
        image = ImageCaptcha(width = 280, height = 90)
        textCaptcha = str(liczba1)+"*"+str(liczba2)
        titleCaptcha = textCaptcha+".png"
        data = image.generate(textCaptcha)
        image.write(textCaptcha, titleCaptcha)
        embed = discord.Embed(colour=discord.Colour.blue(),title=f"Pytanie 2",description="Prosimy abyś rozwiązał(a) to proste równanie (zawsze to będzie mnożenie). Zapisz wynik liczbowo np. `20`")
        if usun==True:
            usun=False
            await channel.purge(limit=2)
        await channel.send(embed=embed)
        await channel.send(file=discord.File(titleCaptcha))
        os.remove(titleCaptcha)
        message = await bot.wait_for("message")
        input = message.content
        if input==str(wynik):
            logiWeryfikacja+="**Pytanie 2**\nRównanie: "+str(liczba1)+"+"+str(liczba2)+"\nOdpowiedź: `"+input+"`\nOdpowiedziano poprawnie. \n\n"
            await channel.purge(limit=1000)
            await pytanieTrzy()
        else:
            logiWeryfikacja+="**Pytanie 2**\nRównanie: "+str(liczba1)+"+"+str(liczba2)+"\nOdpowiedź: `"+input+"`\nOdpowiedziano niepoprawnie.\n\n"
            embed = discord.Embed(colour=discord.Colour.blue(),title=f"Niepoprawna odpowiedź, spróbuj ponownie!",description="Pamiętaj aby zapisać wynik liczbowo np. `12` !")
            await channel.send(embed=embed)
            await pytanieDwa(usun)
            
    # Pytanie 1
    async def pytanieJedenOdp(good):
        nonlocal stopZegar
        if good==False:
            await channel.delete()
            try:
                await member.send("Na serwerze przyjmujemy osoby od 16 roku życia. Weryfikacja nieudana.")
            except:
                pass
            await member.kick(reason="Nieudana weryfikacja. Wiek poniżej 16 lat.")
            stopZegar=True
        
        elif good==True:
            usun=True
            await pytanieDwa(usun)
    embed = discord.Embed(colour=discord.Colour.blue(),title=f"Pytanie 1" ,description="Ile masz lat? Naciśnij guzik najbardziej pasujący do ciebie.")
    class MyView(discord.ui.View):
        @discord.ui.button(label="13-15", row=0, style=discord.ButtonStyle.primary)
        async def first_button(self, button, interaction):
            nonlocal logiWeryfikacja
            logiWeryfikacja+="**Pytanie 1**\nWiek\nOdpowiedź: `13-15`\n\n**Weryfikacja nieudana!**"
            await sendLogiWeryfikacja()
            good=False
            await pytanieJedenOdp(good)
        @discord.ui.button(label="16-25", row=0, style=discord.ButtonStyle.primary)
        async def second_button(self, button, interaction):
            nonlocal logiWeryfikacja
            logiWeryfikacja+="**Pytanie 1**\nWiek\nOdpowiedź: `16-25`\n\n"
            good=True
            await pytanieJedenOdp(good)
        @discord.ui.button(label="26-35", row=0, style=discord.ButtonStyle.primary)
        async def third_button(self, button, interaction):
            nonlocal logiWeryfikacja
            logiWeryfikacja+="**Pytanie 1**\nWiek\nOdpowiedź: `26-35`\n\n"
            good=True
            await pytanieJedenOdp(good)
        @discord.ui.button(label="36-45", row=0, style=discord.ButtonStyle.primary)
        async def four_button(self, button, interaction):
            nonlocal logiWeryfikacja
            logiWeryfikacja+="**Pytanie 1**\nWiek\nOdpowiedź: `36-45`\n\n"
            good=True
            await pytanieJedenOdp(good)
        @discord.ui.button(label="45+", row=0, style=discord.ButtonStyle.primary)
        async def five_button(self, button, interaction):
            nonlocal logiWeryfikacja
            logiWeryfikacja+="**Pytanie 1**\nWiek\nOdpowiedź: `45+`\n\n"
            good=True
            await pytanieJedenOdp(good)
    await channel.send(embed=embed, view=MyView())
@bot.event
async def on_member_update(before, after):
    for i in badwords:
        try:
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
        except:
            pass
@bot.event
async def on_member_leave(member):
    for user in databaseClock:
        try:
            if user.get("userId") == member.id:
                databaseClock.remove({"userId":user.get("userId"),"timeToKick":user.get("timeToKick")})
        except:
            pass
    channel = discord.utils.get(bot.get_all_channels(), id=byeChannel)
    await channel.send(f"{member} opuścił(a) nasz serwer. :sob:")
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(bot.get_all_channels(), id=byeChannel)
    await channel.send(f"{member} opuścił(a) nasz serwer. :sob:")
    guild = member.guild
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
        if entry.target == member:
            embed = discord.Embed(colour=discord.Colour.red(),title=f"{member} został wyrzucony")
            embed.add_field(name="Powód:", value=entry.reason)
            embed.add_field(name="ID:", value=member.id)
            KickLogsChannel = bot.get_channel(KickLogsChannelId)
            #await KickLogsChannel.send(embed=embed)
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
    bans.append({"dateBan":str(datetime.datetime.now()),"id":str(member.id),"reason":str(banned_reason),"caughtNick":str(member),"accCreated":str(member.created_at.astimezone())})
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
            embed = discord.Embed(colour=discord.Colour.red(),title=f"{member} został zbanowany")
            embed.add_field(name="Powód:", value=entry.reason)
            embed.add_field(name="ID:", value=member.id)
            BanLogsChannel = bot.get_channel(BanLogsChannelId)
            #await BanLogsChannel.send(embed=embed)
    for user in databaseClock:
        try:
            if user.get("userId") == member.id:
                databaseClock.remove({"userId":user.get("userId"),"timeToKick":user.get("timeToKick")})
        except:
            pass
@bot.event
async def on_message(message):
    global DoAutomodMessages
    global AdminRoleID
    await dodajXP(int(len(message.content)/5),str(message.author.id))
    wiad = message.content
    for i in ["dzięki","dzieki","dzienki","thx","dziękuję","dziekuje","dziękuje"]:
        if i in wiad.lower():
            await dodajXP(10,str(message.author.id))
    for i in databaseClock:
        if message.author.id == i.get("userId"):
                i["timeToKick"] = Account_IdleTime
    if message.author.bot == False:
        if "siema" in wiad.lower():
            await message.channel.send("No siema :grinning:", reference=message)
        elif "hej" in wiad.lower():
            await message.channel.send("No hej :grinning:", reference=message)
        elif "hejka" in wiad.lower():
            await message.channel.send("No hejka :grinning:", reference=message)
        elif "witam" in wiad.lower():
            await message.channel.send("Witam, witam :grinning:", reference=message)
        elif "cześć" in wiad.lower():
            await message.channel.send("Cześć, cześć :grinning:", reference=message)
    if DoAutomodMessages:
        await checkMessage(message)
    #try:
     #   if message.interaction.name == "bump":
      #      await asyncio.sleep(7200)
       #     BumpChannel= bot.get_channel(BumpChannelID)
        #    role = discord.utils.get(message.guild.roles, id=AdminRoleID)
         #   await BumpChannel.send(f"Czas zrobić bump {role.mention}!")
    #except:
     #   pass
    if message.channel.id in PhothosChannels and len(message.attachments)==0 and message.author.bot == False:
        await message.delete()


@bot.event
async def on_message_edit(before, after):
    global DoAutomodMessages
    if DoAutomodMessages:
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


#@tree.command(name = "mandat", description = "Ukaraj kogoś paroma punktami", guild=discord.Object(id=ServerID)) 
#@discord.app_commands.checks.has_role(AdminRoleID)
#async def mandat(interaction: discord.Interaction, uzytkownik: discord.Member, ilosc: int, powod: str):
#    addPoints(uzytkownik, ilosc)
#    await check(uzytkownik)
#    embed = discord.Embed(colour=discord.Colour.red(),title=f"{uzytkownik.mention} otrzymałeś(aś) mandat za nieprzestrzeganie regulaminu.")
#    embed.add_field(name="Powód:", value=powod)
#    embed.add_field(name="Ilość punktów:", value=str(ilosc))
#    embed.add_field(name="Mandat wlepił:", value=str(interaction.user))
#    for i in database:
#        if i.get("name")==uzytkownik.id:
#            embed2 = discord.Embed(colour=discord.Colour.red(),title=f"Twoja kartoteka obecnie:")
#            embed2.add_field(name="Punkty:", value=str(i.get('points')))
#            if i.get("warnings")==None:
#                warnings=0
#            else:
#                warnings=i.get("warnings")
#            embed2.add_field(name="Ostrzeżenia:", value=str(warnings))
#    LogsChannel = bot.get_channel(LogsChannelId)
#    await LogsChannel.send(embed=embed)
#    await interaction.channel.send(embed=embed2)
#    await interaction.response.send_message(embed=embed)
#@mandat.error
#async def error_mandat(interaction, x):
#    await interaction.response.send_message(f"(/mandat) Brak uprawnień, {interaction.user.mention}")
#@tree.command(name = "daruj-kare", description = "Usun parę punktów z czyjegoś konta", guild=discord.Object(id=ServerID)) 
#@discord.app_commands.checks.has_role(AdminRoleID)
#async def darujKare(interaction: discord.Interaction, uzytkownik: discord.Member, ilosc: int):
#    czy_isnieje = False
#    for i in database:
#        if uzytkownik.id == i.get("name"):
#            if i.get("points") <= ilosc:
#                i["points"]=0
#            else:
#                i["points"]-=ilosc
#            save()
#            await check(uzytkownik)
#            LogsChannel = bot.get_channel(LogsChannelId)
#            await LogsChannel.send(f"{interaction.user.mention} odjął punkty użytkownikowi {uzytkownik.mention}. Liczba odjętych punktów: {ilosc}.")
#            await interaction.response.send_message(f"{interaction.user.mention},odjęto punkty użytkownikowi {uzytkownik.mention}. Liczba odjętych punktów: {ilosc}.")
#            czy_isnieje = True
#    if czy_isnieje == False:
#            await interaction.response.send_message("Brak użytkownika w bazie danych.")
#@darujKare.error
#async def error_darujKare(interaction, x):
#    await interaction.response.send_message(f"(/daruj-kare) Brak uprawnień, {interaction.user.mention}")
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

@tree.command(name = "automod", description = "Przestaw ustawienia automoda wiadomości", guild=discord.Object(id=ServerID)) 
@discord.app_commands.checks.has_role(AdminRoleID)
@discord.app_commands.choices(przelacz=[
    discord.app_commands.Choice(name='Włącz', value="Włącz"),
    discord.app_commands.Choice(name='Wyłącz', value="Wyłącz")])

async def switchAutomod(interaction: discord.Interaction, przelacz: discord.app_commands.Choice[str]):
    global DoAutomodMessages
    if przelacz.value=="Włącz":
        DoAutomodMessages = True
        config["DoAutomodMessages"]= True
        file = open("config.json","w")
        file.write(json.dumps(config))
        file.close()
        await interaction.response.send_message("Sprawdzanie wiadomości włączone!")
    elif przelacz.value=="Wyłącz":
        DoAutomodMessages = False
        config["DoAutomodMessages"]= False
        file = open("config.json","w")
        file.write(json.dumps(config))
        file.close()
        await interaction.response.send_message("Sprawdzanie wiadomości wyłączone!")
@switchAutomod.error
async def error_switchAutomod(interaction, x):
    await interaction.response.send_message(f"(/automod) Brak uprawnień, {interaction.user.mention}")

@tree.command(name = "zaszyfruj", description = "Zaszyfruj dany tekst", guild=discord.Object(id=ServerID)) 
@discord.app_commands.choices(standard=[
    discord.app_commands.Choice(name='Base64', value="Base64"),
    discord.app_commands.Choice(name='Fernet', value="Fernet")])
async def zaszyfruj(interaction: discord.Interaction, standard: discord.app_commands.Choice[str],wartosc: str,klucz: str=None):
    if standard.value=="Fernet" and klucz==None:
        await interaction.response.send_message("Standard Fernet wymaga podania klucza (32 url-safe base64). Nie posiadasz klucza? Wygeneruj komendą (/generuj-klucz).")
    if wartosc!=None:
        wartosc=wartosc.encode()
    if standard.value=="Fernet":
        klucz=klucz.encode()
        zaszyfrowany = Fernet(klucz).encrypt(wartosc)
        await interaction.response.send_message(zaszyfrowany.decode())
    elif standard.value=="Base64":
        zaszyfrowany = base64.b64encode(wartosc)
        await interaction.response.send_message(zaszyfrowany.decode())
@zaszyfruj.error
async def error_zaszyfruj(interaction, x):
    await interaction.response.send_message("Prawdopodobnie podałeś klucz niezgodny z standardem Fernet, albo coś innego poszło nie tak. Wygeneruj klucz komendą (/generuj-klucz)")


@tree.command(name = "odszyfruj", description = "Odszyfruj dany tekst", guild=discord.Object(id=ServerID)) 
@discord.app_commands.choices(standard=[
    discord.app_commands.Choice(name='Base64', value="Base64"),
    discord.app_commands.Choice(name='Fernet', value="Fernet")])
async def odszyfruj(interaction: discord.Interaction, standard: discord.app_commands.Choice[str],wartosc: str,klucz: str=None):
    if standard.value=="Fernet" and klucz==None:
        await interaction.response.send_message("Standard Fernet wymaga podania klucza którym zaszyfrowano tekst.")
    if wartosc!=None:
        wartosc=wartosc.encode()
    if standard.value=="Fernet":
        klucz=klucz.encode()
        odszyfrowany = Fernet(klucz).decrypt(wartosc)
        await interaction.response.send_message(odszyfrowany.decode())
    elif standard.value=="Base64":
        odszyfrowany = base64.b64decode(wartosc)
        await interaction.response.send_message(odszyfrowany.decode())
@odszyfruj.error
async def error_odszyfruj(interaction, x):
    await interaction.response.send_message("Jeżeli wybrałeś standard Base64, prawdopodobnie podałeś niepopraną wartość. Jeżeli twoim standardem jest Fernet podałeś niepoprawny klucz lub wartość.")


@tree.command(name = "generuj-klucz", description = "Wygeneruj klucz potrzebny do szyfrowania.", guild=discord.Object(id=ServerID)) 
@discord.app_commands.choices(standard=[
    discord.app_commands.Choice(name='Fernet', value="Fernet")])
async def generujKlucz(interaction: discord.Interaction, standard: discord.app_commands.Choice[str]):
    if standard.value=="Fernet":
        klucz=Fernet.generate_key()
        await interaction.response.send_message(klucz.decode())

@tree.command(name = "dodaj-xp", description = "Dodaje xp", guild=discord.Object(id=ServerID)) 
@discord.app_commands.checks.has_role(AdminRoleID)
async def dajtaXP(interaction: discord.Interaction, uzytkownik: discord.Member, ilosc: int):
    await dodajXP(ilosc,str(uzytkownik.id))
    embed = discord.Embed(colour=discord.Colour.green(),title=f"Dodano punkty użytkownikowi {uzytkownik}")
    embed.add_field(name="Ilość:", value=str(ilosc))
    await interaction.response.send_message(embed=embed)
@dajtaXP.error
async def dajtaXPError(interaction,x):
    await interaction.response.send_message("Brak uprawnień.")
@tree.command(name = "ranking", description = "Pokazuje ranking", guild=discord.Object(id=ServerID)) 
async def ranking(interaction: discord.Interaction):
    sql="SELECT * FROM levele ORDER BY xp DESC LIMIT 10"
    mycursor.execute(sql)
    myresults = mycursor.fetchall()
    embed = discord.Embed(colour=discord.Colour.blue(),title=f"Ranking")
    licznik=1
    for result in myresults:
        user = bot.get_user(int(result[0]))
        embed.add_field(name=f"**{licznik}. {user}**", value=f"Punkty doświadczenia: {result[1]}\nPoziom: {result[2]}",inline=False)
        licznik+=1
    await interaction.response.send_message(embed=embed)
@tree.command(name = "moj-poziom", description = "Pokazuje twój poziom", guild=discord.Object(id=ServerID)) 

async def mojPoziom(interaction: discord.Interaction):
    sql="SELECT * FROM levele WHERE discordid=%s"
    val=[(str(interaction.user.id))]
    mycursor.execute(sql,val)
    myresults = mycursor.fetchall()
    if myresults!=[]:
        embed = discord.Embed(colour=discord.Colour.gold(),title=f"{interaction.user.display_name}, oto twoje osiągnięcia:")
        embed.add_field(name=f"Punkty Doświadczenia:", value=f"{myresults[0][1]}")
        embed.add_field(name=f"Poziom:", value=f"{myresults[0][2]}")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(colour=discord.Colour.red(),title=f"{interaction.user.display_name}, nie posiadasz punktów doświadczeń! Pisz dalej :)")
        await interaction.response.send_message(embed=embed)

@tree.command(name = "embed", description = "Wysyła wiadomość jako embed na wybranym kanale.", guild=discord.Object(id=ServerID)) 
@discord.app_commands.checks.has_role(AdminRoleID)
async def sendEmbed(interaction: discord.Interaction, tytul: str, tresc: str, kanal: discord.TextChannel):
    embed = discord.Embed(colour=discord.Colour.blue(),title=tytul,description=tresc)
    await kanal.send(embed=embed)
    await interaction.response.send_message("Wysłano :)")
@sendEmbed.error
async def errorSendEmbed(interaction,x):
    await interaction.response.send_message("Brak uprawnień.")
@tree.command(name = "generuj-obrazek", description = "AI wygeneruje 9 obrazków.", guild=discord.Object(id=ServerID)) 
@discord.app_commands.choices(styl=[
        discord.app_commands.Choice(name="Sztuka", value="art"),
        discord.app_commands.Choice(name="Rysunek", value="drawing"),
        discord.app_commands.Choice(name="Zdjęcie", value="photo"),
        discord.app_commands.Choice(name="Bez stylu", value="none")
        ])
async def genWallpaper(interaction: discord.Interaction,motyw: str, styl: discord.app_commands.Choice[str]="art"):
    await interaction.response.defer()
    wiad = await interaction.channel.send("Trwa generowanie twojego zestawu obrazków. Potrwa to około minutę.")
    if type(styl)!=str:
        generated_images = await generator.async_generate(motyw,model_type=styl.value)
    else:
        generated_images = await generator.async_generate(motyw,model_type=styl)
    b64_list = await craiyon_utils.async_encode_base64(generated_images.images)
    images1 = []
    for index, image in enumerate(b64_list): # Loop through b64_list, keeping track of the index
        img_bytes = BytesIO(base64.b64decode(image)) # Decode the image and store it as a bytes object
        image = discord.File(img_bytes)
        image.filename = f"result{index}.png"
        images1.append(image)
    await interaction.followup.send(files=images1)
    await wiad.delete()
def backup():
    dzisiejszadata=datetime.datetime.today().date()
    timez=datetime.datetime.now().time()
    timez = timez.replace(microsecond=0)
    naglowek=str(dzisiejszadata)+"*"+str(timez)
    os.system("mkdir backup"+naglowek)
    os.system("cp bot.py backup"+naglowek+"/bot.py")
    os.system("cp bans.json backup"+naglowek+"/bans.json")
    os.system("cp database.json backup"+naglowek+"/database.json")
    os.system("cp databaseClock.json backup"+naglowek+"/databaseClock.json")
    os.system("cp standby.py backup"+naglowek+"/standby.py")
    os.system("cp time.json backup"+naglowek+"/time.json")
    os.system("cp requirements.txt backup"+naglowek+"/requirements.txt")
    try:
        sql= "SELECT * FROM levele"
        mycursor.execute(sql)
        results = mycursor.fetchall()
        plik = open("leveleBackup.json","x")
        plik.close()
        plik = open("leveleBackup.json","w")
        plik.write(json.dumps(results))
        plik.close()
        os.system("cp leveleBackup.json backup"+naglowek+"/leveleBackup.json")
        os.system("rm leveleBackup.json")
    except:
        print("Błąd bazy danych. Pomijam.")
    remoteFolderMetaData = {
    'title': str(naglowek),
    'parents': [{"id":BackupFolderGDID}],
    'mimeType': 'application/vnd.google-apps.folder'
    }
    remoteFolder = drive.CreateFile(remoteFolderMetaData)
    remoteFolder.Upload()
    remoteFolderId = remoteFolder['id']
    filesList=os.listdir("backup"+naglowek+"/")
    os.chdir("backup"+naglowek)
    for file in filesList:
        template = drive.CreateFile({"parents": [{"id": remoteFolderId}]})
        template.SetContentFile(file)
        template.Upload()
    os.chdir("..")
    os.system("rm -r backup"+naglowek)
    print("Wykonano backup")
generator = Craiyon()
gauth = GoogleAuth()
gauth.LoadCredentialsFile("gauth.json")
if gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
drive = GoogleDrive(gauth)
backup()
load()

bot.run(TOKEN)
