from tortoise import Tortoise
from config import config


class Database:
    
    @staticmethod
    async def init():
        await Tortoise.init (
            db_url = config.database_url,
            modules = {
                "models": [
                    "auth.models",
                    "chat.models",
                ]
            }
        )

        await Tortoise.generate_schemas(safe=True)

    @staticmethod
    async def close():
        await Tortoise.close_connections()
