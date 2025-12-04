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
    await bot.wait_until_ready()  # รอให้ bot พร้อม
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        print(f"ไม่พบ channel ID {channel_id}")

# ==========================
# ฟังก์ชันทดสอบ ส่งทันที
# ==========================
async def send_test_alert():
    test_channel_id = 1445995017092202618  # ใส่ Channel ID ของคุณ
    message = f"นี่คือข้อความแจ้งเตือนทดสอบ! เวลาปัจจุบัน: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    await send_alert(message, test_channel_id)

# ==========================
# ฟังก์ชันแจ้งเตือนรายวัน
# ==========================
async def send_daily_alert():
    daily_channel_id = 1425309010487279616  # ใส่ Channel ID ของคุณ
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
    print(f"Command !now ถูกเรียกโดย {ctx.author}")

# ==========================
# Command: เทสกิจกรรม
# ==========================
@bot.command()
async def test_events(ctx):
    await send_test_alert()
    await ctx.send("ทดสอบเรียบร้อย ✅")
    print(f"Command !test_events ถูกเรียกโดย {ctx.author}")

# ==========================
# รัน bot
# ==========================
bot.run(TOKEN)

