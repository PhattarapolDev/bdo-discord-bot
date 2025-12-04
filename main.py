import os
import discord
from discord.ext import commands

# ดึง TOKEN จาก Environment Variable
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("TOKEN ไม่ได้ตั้งค่าใน Environment Variable!")

# ตั้ง Intents (เปิด message content intent ด้วยถ้าต้องการอ่านข้อความ)
intents = discord.Intents.default()
intents.message_content = True  # สำหรับ command / on_message

# สร้าง bot
bot = commands.Bot(command_prefix="!", intents=intents)

# ตัวอย่าง Event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# ตัวอย่าง Command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# รัน bot
bot.run(TOKEN)
