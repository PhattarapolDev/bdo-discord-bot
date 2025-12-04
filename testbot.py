import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

# ==========================
# ตั้งค่า TOKEN
# ==========================
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("TOKEN ไม่ได้ตั้งค่าใน Environment Variable!")

# ==========================
# ตั้งค่า intents และ bot
# ==========================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# Scheduler
# ==========================
scheduler = AsyncIOScheduler()

# ==========================
# ฟังก์ชันแจ้งเตือน
# ==========================
async def send_alert(message: str, channel_id: int):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)

# ==========================
# ฟังก์ชันทดสอบ ส่งทันที
# ==========================
async def send_test_alert():
    test_channel_id = 1445995017092202618  # ใส่ Channel ID ของคุณ
    message = "นี่คือข้อความแจ้งเตือนทดสอบ! เวลาปัจจุบัน: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await send_alert(message, test_channel_id)

# ==========================
# ฟังก์ชันแจ้งเตือนรายวัน
# ==========================
async def send_daily_alert():
    # ตัวอย่าง: ข้อความจริงที่อยากแจ้ง
    daily_channel_id = 1445995017092202618  # ใส่ Channel ID ของคุณ
    # ตัวอย่างดึงข้อมูลกิจกรรมจาก JSON หรือ DB
    # กำหนด message เองตอนนี้
    message = "สวัสดี! นี่คือกิจกรรมที่กำลังจะหมดในวันนี้ (ตัวอย่าง)"
    await send_alert(message, daily_channel_id)

# ==========================
# Event: on_ready
# ==========================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

    # Scheduler: เทสส่งทันทีตอนบอทรัน
    scheduler.add_job(send_test_alert, 'date', run_date=datetime.now() + timedelta(seconds=5))

    # Scheduler: ตั้งเวลาแจ้งเตือนทุกวัน 9 โมงเช้า
    scheduler.add_job(send_daily_alert, 'cron', hour=9, minute=0)

    scheduler.start()

# ==========================
# Command: ตรวจสอบเวลาปัจจุบัน
# ==========================
@bot.command()
async def now(ctx):
    await ctx.send(f"เวลาปัจจุบัน: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ==========================
# Command: เทสกิจกรรม
# ==========================
@bot.command()
async def test_events(ctx):
    await send_test_alert()
    await ctx.send("ทดสอบเรียบร้อย ✅")

# ==========================
# รัน bot
# ==========================
bot.run(TOKEN)
