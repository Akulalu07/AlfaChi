from tortoise import Tortoise
from config import settings

async def init_db():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={
            "models": [
                "auth.models",
                "chat.models",
            ]
        }
    )
    # safe=True создает только новые таблицы, если их нет
    # После удаления volume БД, создастся новая схема с правильной структурой
    await Tortoise.generate_schemas(safe=True)

async def close_db():
    await Tortoise.close_connections()

