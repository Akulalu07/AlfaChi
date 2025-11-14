import asyncio
import logging
import aiohttp
import os
from aiogram import Bot, Dispatcher
from backend_service import http_service
from aiogram.enums import ParseMode
from handlers.user_handlers import router as user_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    bot_token = os.getenv("BOT_TOKEN", "")
    
    if not bot_token:
        logger.error("BOT_TOKEN не установлен!")
        return
    
    bot = Bot(
        token=bot_token
    )
    dp = Dispatcher()
    
    dp.startup.register(http_service.get_session)
    dp.shutdown.register(http_service.close_session)
    
    dp.include_router(user_router)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

