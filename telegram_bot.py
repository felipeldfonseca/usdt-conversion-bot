from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
from cotation_service import get_cotation
from lock_manager import lock_quote
from pix_simulator import confirm_pix
from trade_simulator import execute_trade

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Welcome! Type /convert to start a BRL ↔ USDT conversion.")

@bot.on(events.NewMessage(pattern='/convert'))
async def convert(event):
    price = get_cotation()
    await event.respond(f"Current rate: 1 USDT = R${price}\nType amount in BRL:")

    @bot.on(events.NewMessage)
    async def receive_amount(e):
        try:
            amount = float(e.raw_text.strip())
            usdt = round(amount / price, 4)
            lock = lock_quote(e.sender_id, amount, usdt, price)
            await e.respond(f"Locked quote: R${amount} = {usdt} USDT\nSend PIX now to chave: pix@teste.com")

            if confirm_pix(e.sender_id):
                result = execute_trade(amount, usdt)
                await e.respond(f"✅ Trade executed! Sent {usdt} USDT. TxID: {result}")
            else:
                await e.respond("⚠️ PIX not confirmed in time. Quote expired.")
        except ValueError:
            await e.respond("Invalid amount. Try again.")

def start_bot():
    bot.run_until_disconnected() 