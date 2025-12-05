import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.db import DB
from utils.ton_checker import check_payments
from utils.ai import generate_text, summarize_text, generate_image

# تنظیمات
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))  # جایگزین کن با آیدی تلگرامی خودت

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = DB()

# پردازش پرداخت
async def on_payment(user_id, tx_hash, amount):
    # در نسخه پیشرفته: پیدا کردن کاربر از طریق comment یا لینک
    # الان: ارسال به همه — یا می‌تونی این قسمت رو برای نسخه V2 بذاری
    pass

# دستور شروع
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    ref = message.text.split()
    ref_by = None
    if len(ref) > 1 and ref[1].startswith("u_"):
        ref_by = int(ref[1][2:])
    db.create_user(user_id, ref_by)

    kb = InlineKeyboardBuilder()
    kb.button(text="🛍️ خرید محصولات", callback_data="shop")
    kb.button(text="✨ تولید محتوا", callback_data="ai_menu")
    kb.button(text="📤 لینک شخصی", callback_data=f"share_{user_id}")
    kb.adjust(1)

    await message.answer(
        "🤖 سلام! من NinjaAiBot هستم.\n"
        "• محصولات دیجیتال بفروش\n"
        "• محتوا تولید کن\n"
        "• پول دریافت کن — همه چیز خودکار!",
        reply_markup=kb.as_markup()
    )

# فروشگاه
@dp.callback_query(F.data == "shop")
async def shop(call: types.CallbackQuery):
    products = db.get_products()
    kb = InlineKeyboardBuilder()
    for p in products:
        kb.button(text=f"{p[1]} - ${p[2]}", callback_data=f"buy_{p[0]}")
    kb.button(text="« بازگشت", callback_data="start")
    kb.adjust(1)
    await call.message.edit_text("🛒 محصولات موجود:", reply_markup=kb.as_markup())

# تولید محتوا
@dp.callback_query(F.data == "ai_menu")
async def ai_menu(call: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 تولید متن", callback_data="gen_text")
    kb.button(text="🔍 خلاصه‌نویسی", callback_data="summarize")
    kb.button(text="🖼️ تولید تصویر", callback_data="gen_image")
    kb.button(text="« بازگشت", callback_data="start")
    kb.adjust(1)
    await call.message.edit_text("✨ انتخاب کن:", reply_markup=kb.as_markup())

# پنل ادمین
@dp.message(Command("addproduct"))
async def add_product(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("دستور اضافه‌کردن محصول فعال شد (در نسخه کامل پیاده‌سازی می‌شه).")

@dp.message(Command("stats"))
async def stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    # آمار ساده
    c = db.conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    users = c.fetchone()[0]
    c.execute("SELECT COUNT(*), SUM(amount) FROM sales")
    sales_count, revenue = c.fetchone()
    await message.answer(f"📊 آمار:\nکاربران: {users}\nفروش: {sales_count}\nدرآمد: ${revenue or 0}")

# پرداخت
@dp.callback_query(F.data.startswith("buy_"))
async def buy(call: types.CallbackQuery):
    await call.message.answer(
        "✅ برای خرید، لطفاً **۹.۹۹ USDT** رو روی **شبکه TON** به آدرس زیر بفرستید:\n\n"
        "`UQDaR6-bXwwh9fkBA3o-zdnPvRhV5cUJkCjnO4et90MgfLQN`\n\n"
        "پس از پرداخت، ربات خودکار PDF رو برات ارسال می‌کنه.",
        parse_mode="Markdown"
    )

# لینک دعوت
@dp.callback_query(F.data.startswith("share_"))
async def share(call: types.CallbackQuery):
    uid = call.data.split("_")[1]
    link = f"https://t.me/NinjaAiBot?start=u_{uid}"
    await call.message.answer(f"📤 لینک شخصی تو:\n{link}\n\nهر خرید از این لینک، ثبت می‌شه!")

async def main():
    # شروع چک پرداخت در پس‌زمینه
    asyncio.create_task(check_payments(on_payment))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())