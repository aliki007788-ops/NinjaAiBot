import requests
import asyncio
from collections import defaultdict

TON_API = "https://toncenter.com/api/v2/getTransactions"
ADDRESS = "UQDaR6-bXwwh9fkBA3o-zdnPvRhV5cUJkCjnO4et90MgfLQN"
MIN_AMOUNT_USDT = 9.99 * 1_000_000  # USDT-TON در واحد میکرو

# ذخیره آدرس‌هایی که قبلاً پرداخت کردن
processed_txs = set()

async def check_payments(callback_on_payment):
    while True:
        try:
            res = requests.get(TON_API, params={"address": ADDRESS, "limit": 10})
            if res.status_code == 200:
                txs = res.json().get("result", [])
                for tx in txs:
                    tx_hash = tx["transaction_id"]["hash"]
                    if tx_hash in processed_txs:
                        continue
                    # بررسی آیا ورودی است
                    if tx.get("in_msg") and "value" in tx["in_msg"]:
                        value = int(tx["in_msg"]["value"])
                        if value >= MIN_AMOUNT_USDT:
                            # پیدا کردن کاربر (از طریق comment یا لینک دعوت)
                            user_id = None  # در نسخه پیشرفته از comment استفاده می‌شه
                            await callback_on_payment(user_id, tx_hash, value / 1_000_000)
                            processed_txs.add(tx_hash)
        except Exception as e:
            print(f"TON Check Error: {e}")
        await asyncio.sleep(10)