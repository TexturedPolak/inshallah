import discord
from discord.ext import commands
import time
import asyncio
from discord.ext.commands import has_permissions, CheckFailure
admins_role_id=0 #admin_role_id
id_serwa=0 #server_id
TOKEN=""
intents=discord.Intents.all()
discord.member = True
intents.message_content = True
bot = discord.Client( intents=intents, case_insensitive=True)
tree = discord.app_commands.CommandTree(bot)
@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=id_serwa))
    print("I'm ready!")
@bot.event
async def on_member_join(member):
    print(member.created_at.timestamp(), time.time())
    if time.time() - member.created_at.timestamp() < 7_890_000 : #3 miesiące w sekundach
        await member.send("Twoje konto zostało uznane za skrajnie podejrzane. Spróbuj ponownie kiedy indziej :)")
        await member.kick(reason="Fresh account")

@bot.event
async def on_message(message):
    if message.content.lower() == "siema":
        await message.channel.send("No siema :)", reference=message)


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
bot.run(TOKEN)
