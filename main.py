import discord
from discord.ext import commands
import os
from dotenv import load_dotenv  # อ่านไฟล์ .env

# โหลดไฟล์ .env (ต้องมีไฟล์ .env ในโฟลเดอร์เดียวกับ main.py)
load_dotenv()

# ดึง token จาก environment
TOKEN = os.getenv("DISCORD_TOKEN")

# ตั้ง intents ให้ bot อ่านข้อความได้
intents = discord.Intents.default()
intents.message_content = True

# สร้าง bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")

# ตัวอย่าง command
@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

# รัน bot
print("TOKEN =", TOKEN[:4], "..." if TOKEN else "None")
bot.run(TOKEN)
