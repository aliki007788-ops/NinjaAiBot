# database.py
import os
import aiosqlite
from datetime import datetime

# تعیین مسیر دیتابیس: در Render از دیسک دائمی استفاده می‌شود
if os.getenv("RENDER"):
    DB_NAME = "/var/lib/data/ninja_pro.db"
else:
    DB_NAME = "ninja_pro.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # جدول کاربران
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                referrer_id INTEGER,
                balance REAL DEFAULT 0,
                joined_at TEXT
            )
        """)
        # جدول سفارشات
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                user_id INTEGER,
                amount REAL,
                status TEXT DEFAULT 'pending',
                created_at TEXT
            )
        """)
        await db.commit()

async def add_user(user_id, username, referrer_id=None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, referrer_id, joined_at) VALUES (?, ?, ?, ?)",
            (user_id, username, referrer_id, datetime.now().isoformat())
        )
        await db.commit()

async def create_order(order_id, user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO orders (order_id, user_id, amount, created_at) VALUES (?, ?, ?, ?)",
            (order_id, user_id, amount, datetime.now().isoformat())
        )
        await db.commit()

async def get_pending_orders():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT order_id, user_id, amount FROM orders WHERE status = 'pending'") as cursor:
            return await cursor.fetchall()

async def mark_order_paid(order_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE orders SET status = 'paid' WHERE order_id = ?", (order_id,))
        await db.commit()