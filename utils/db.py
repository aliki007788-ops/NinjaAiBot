import sqlite3
from datetime import datetime

class DB:
    def __init__(self, path="ninja.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.init_db()

    def init_db(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                ref_by INTEGER,
                lang TEXT DEFAULT 'en'
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL,
                file_id TEXT,
                description TEXT,
                media_type TEXT DEFAULT 'file'
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                tx_hash TEXT,
                amount REAL,
                time TEXT
            )
        """)
        # محصول نمونه
        c.execute("SELECT COUNT(*) FROM products")
        if c.fetchone()[0] == 0:
            c.execute("""
                INSERT INTO products (name, price, file_id, description, media_type)
                VALUES (?, ?, ?, ?, ?)
            """, ("10助推 Prompt (Grok-4)", 9.99, "PDF_100_GROK", "100 advanced prompts for Grok-4 AI to generate million-dollar SaaS ideas", "file"))
        self.conn.commit()

    def get_user(self, user_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return c.fetchone()

    def create_user(self, user_id, ref_by=None):
        c = self.conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (id, ref_by) VALUES (?, ?)", (user_id, ref_by))
        self.conn.commit()

    def get_products(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM products")
        return c.fetchall()

    def log_sale(self, user_id, product_id, tx_hash, amount):
        c = self.conn.cursor()
        c.execute("INSERT INTO sales (user_id, product_id, tx_hash, amount, time) VALUES (?, ?, ?, ?, ?)",
                  (user_id, product_id, tx_hash, amount, datetime.utcnow().isoformat()))
        self.conn.commit()