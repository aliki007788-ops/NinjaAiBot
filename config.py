# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
    WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
    WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ninja-bot-pro.onrender.com")
    PRODUCT_PRICE = 9.99