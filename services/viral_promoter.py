# services/viral_promoter.py
from telethon import TelegramClient
import asyncio
import random
import os

# مسیر session: در Render باید روی دیسک دائمی ذخیره شود
SESSION_FILE = "/var/lib/data/ninja_promoter_session" if os.getenv("RENDER") else "ninja_promoter_session"

API_ID = os.getenv("APP_API_ID")
API_HASH = os.getenv("APP_API_HASH")
PHONE = os.getenv("APP_PHONE")

ADS_TEXT = [
    "🚀 بهترین ابزار هوش مصنوعی برای بیزینس!\nهمین الان تست کن: @NinjaAiBot",
    "دنبال درآمد دلاری هستی؟ 💵\nربات نینجا رو ببین: @NinjaAiBot",
]

TARGET_GROUPS = os.getenv("TARGET_GROUPS", "").split(",") if os.getenv("TARGET_GROUPS") else []

async def start_promoter():
    if not API_ID or not API_HASH or not PHONE:
        print("Promoter info not fully set. Skipping promoter.")
        return

    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)

    await client.start(phone=PHONE)
    print("✅ Promoter Started…")

    while True:
        try:
            for group in TARGET_GROUPS:
                try:
                    msg = random.choice(ADS_TEXT)
                    await client.send_message(group.strip(), msg)
                    print(f"Sent ad to {group}")
                    # وقفه امن: بین 1 تا 3 ساعت
                    await asyncio.sleep(random.randint(3600, 10800))
                except Exception as e:
                    print(f"Error sending to {group}: {e}")
                    await asyncio.sleep(600)  # 10 دقیقه در صورت خطا
            # استراحت کلی قبل از چرخهٔ بعدی
            await asyncio.sleep(7200)
        except Exception as e:
            print(f"Promoter loop error: {e}")
            await asyncio.sleep(3600)