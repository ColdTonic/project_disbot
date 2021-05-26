#Before you run
#Please grab .env file before running. Find this in Discord Developer Portal or contact the bot account's creator
#The Discord Token is required to authenticate connection between client -> discord
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

#Grab environment keys for bot authentication
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Create an instance of bot which users access commands by calling !<command>
client = commands.Bot(command_prefix="!")

#Init bot, display connection success in cmd
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user.name} has connected to discord!\n'
        f'{client.user} is connected to the following guilds:\n'
        f'{guild.name}(id: {guild.id})'
        )

#Load all cogs in /cogs
@client.command(hidden=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

#Unload cogs for error testing
@client.command(hidden=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

#Reload all cog files
@client.command(hidden=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#Send bot client token environment variables
client.run(TOKEN)