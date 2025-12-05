import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiohttp import web
from config import Config
from database import init_db
from handlers import user_panel
from services.payment_monitor import check_ton_transactions
from services.viral_promoter import start_promoter

logging.basicConfig(level=logging.INFO)

async def web_app_handler(request):
    with open("web/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return web.Response(text=content, content_type="text/html")

async def main():
    await init_db()

    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_panel.router)

    asyncio.create_task(check_ton_transactions(bot))
    asyncio.create_task(start_promoter())

    app = web.Application()
    app.router.add_get("/webapp", web_app_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("WebApp Server running on port 8080")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
