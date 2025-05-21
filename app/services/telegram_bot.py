import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import requests
from app.core.config import settings

bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=["status"])
async def send_status(message: types.Message):
    try:
        response = requests.get("http://web:8000/metrics")
        if response.status_code == 200:
            await message.reply("✅ FastAPI service is up and running.")
        else:
            await message.reply("⚠️ FastAPI service is not responding properly.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

def start_bot():
    executor.start_polling(dp, skip_updates=True)