import asyncio

import discord
import os
from discord.ext import commands


INTENTS = discord.Intents.all()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=INTENTS)

@bot.event
async def on_ready():
    print(os.listdir("./app/cogs"))
    print(f'Logged in as {bot.user.name}')

async def load():
    for filename in os.listdir("./app/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"app.cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())
