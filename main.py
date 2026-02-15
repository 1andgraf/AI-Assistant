import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv() 

from ai_concierge.database.db import init_db
from ai_concierge.bot.handlers import router

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    if not TOKEN:
        print("Error: BOT_TOKEN is not set in .env")
        return

    init_db()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    dp.include_router(router)

    print("🤖 AI Concierge Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
