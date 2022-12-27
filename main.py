import discord
from   discord.ext import commands
import asyncio
import json
import bot_commands

with open('config.json', 'r') as cfg:
  # Deserialize the JSON data
  data = json.load(cfg)

client = commands.Bot(command_prefix='.', 
intents = discord.Intents.all())
client.remove_command('help')

async def main():

    async with client:
        await bot_commands.setup(client)
        await client.start(data['token'])

asyncio.run(main())
