import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apps.bot.utils import setup_django

# Load environment variables
load_dotenv()

# Setup Django before importing models
setup_django()

# Import handlers (after django setup)
from apps.bot.handlers import router
from apps.bot.storage import DjangoStorage

async def main():
    logging.basicConfig(level=logging.INFO)
    
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN not found in environment variables")
        
    
    bot = Bot(token=bot_token)
    storage = DjangoStorage()
    dp = Dispatcher(storage=storage)
    
    dp.include_router(router)
    
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
