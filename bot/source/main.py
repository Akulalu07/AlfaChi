from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import asyncio
import os

from stuff import *
from core.handlers import router


async def main():
    bot_token = os.getenv("BOT_TOKEN", None)
    
    if bot_token is None:
        return logger.error("BOT_TOKEN is not set!")
    
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    
    dp.startup.register(backend.get_session)
    dp.shutdown.register(backend.close_session)
    
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
