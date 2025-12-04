import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")  # ดึงจาก Environment Variable

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")

bot.run(TOKEN)
