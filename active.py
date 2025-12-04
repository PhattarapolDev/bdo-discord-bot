import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from discord.ext import commands, tasks

# ดึง TOKEN จาก Environment Variable
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("TOKEN ไม่ได้ตั้งค่าใน Environment Variable!")
    
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# โหลด JSON
def load_activities():
    try:
        with open("activities.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# เซฟ JSON
def save_activities(data):
    with open("activities.json", "w") as f:
        json.dump(data, f, indent=2)

# ฟังก์ชันดึงข่าวจาก BDO
def fetch_activities():
    activities = []
    page = 1
    while True:
        url = f"https://blackdesert.pearlabyss.com/Asia/th-TH/News/Notice?_categoryNo=3&_pageNo={page}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        news = soup.select(".noticeList li")  # ตัวอย่าง selector
        if not news:
            break
        for item in news:
            title = item.select_one(".title").text.strip()
            end_date = item.select_one(".endDate").text.strip()  # สมมุติว่าเว็บมี class นี้
            id_ = item["data-id"]
            activities.append({"id": id_, "title": title, "end_date": end_date, "notified": False})
        page += 1
    return activities

# Task แจ้งเตือน
@tasks.loop(hours=24)
async def daily_check():
    activities = load_activities()
    today = datetime.today().date()
    
    # ตรวจสอบหมดอายุ
    activities = [a for a in activities if datetime.strptime(a["end_date"], "%Y-%m-%d").date() >= today]
    
    # แจ้งเตือนกิจกรรมใกล้หมด
    for a in activities:
        end = datetime.strptime(a["end_date"], "%Y-%m-%d").date()
        if not a["notified"] and (end - today).days <= 1:
            channel = bot.get_channel(YOUR_CHANNEL_ID)
            await channel.send(f"กิจกรรม **{a['title']}** กำลังจะหมดใน {a['end_date']}!")
            a["notified"] = True

    save_activities(activities)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    daily_check.start()

# รัน bot
bot.run(TOKEN)

