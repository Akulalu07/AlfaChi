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

    await Tortoise.generate_schemas(safe=True)

async def close_db():
    await Tortoise.close_connections()

