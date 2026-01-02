import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database.db import db
from handlers.commands import router as commands_router
from handlers.messages import router as messages_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def main():
    # Initialize bot and dispatcher
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Include routers
    dp.include_router(commands_router)
    dp.include_router(messages_router)
    
    # Create database tables
    await db.create_tables()
    logger.info("Database initialized")
    
    # Start polling
    logger.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())