import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# ดึง TOKEN จาก Environment Variable
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("TOKEN ไม่ได้ตั้งค่าใน Environment Variable!")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Scheduler
scheduler = AsyncIOScheduler()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    # ตัวอย่าง: เทสให้แจ้งเตือนทันที
    scheduler.add_job(send_test_alert, 'date', run_date=datetime.now())
    
    # ตัวอย่างจริง: ตั้งเวลาแจ้งเตือนทุกวัน 9 โมงเช้า
    # scheduler.add_job(send_daily_alert, 'cron', hour=9, minute=0)
    
    scheduler.start()

async def send_test_alert():
    channel = bot.get_channel(1445995017092202618)  # ใส่ Channel ID ที่ต้องการโพสต์
    if channel:
        await channel.send("นี่คือข้อความแจ้งเตือนทดสอบ! เวลาปัจจุบัน: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# ตัวอย่าง command
@bot.command()
async def now(ctx):
    await ctx.send(f"เวลาปัจจุบัน: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# รัน bot
bot.run(TOKEN)

