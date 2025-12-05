from telethon import TelegramClient
import random, asyncio, os

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")

client = TelegramClient('promoter', api_id, api_hash)

GROUPS = [
    '@techstartups', '@cryptonewsenglish', '@arabdevs', '@russiantech',
    '@digitalnomads', '@usabusiness', '@middleeasttech'
]

MESSAGES = {
    'en': "🚀 Get 100 advanced Grok-4 prompts to build million-dollar AI SaaS! Only $9.99 → https://t.me/NinjaAiBot",
    'ar': "🚀 احصل على 100 برومبت متقدم لـ Grok-4 لبناء شركات ذكاء اصطناعي بملايين الدولارات! بـ 9.99$ فقط → https://t.me/NinjaAiBot",
    'ru': "🚀 Получи 100 продвинутых промптов для Grok-4, чтобы создать SaaS на миллионы! Всего $9.99 → https://t.me/NinjaAiBot"
}

async def main():
    await client.start(phone)
    while True:
        for group in GROUPS:
            try:
                entity = await client.get_entity(group)
                if hasattr(entity, 'participants_count') and entity.participants_count > 5000:
                    lang = random.choice(list(MESSAGES.keys()))
                    msg = MESSAGES[lang]
                    await client.send_message(entity, msg)
                    delay = random.randint(7200, 14400)  # 2-4 ساعت
                    await asyncio.sleep(delay)
            except Exception as e:
                print(f"Error in {group}: {e}")
                await asyncio.sleep(3600)

asyncio.run(main())