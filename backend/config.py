import os
from typing import Optional

class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "pass")
    DB_NAME: str = os.getenv("DB_NAME", "db")
    
    OPEN_ROUTER_API_KEY: str = os.getenv("OPEN_ROUTER", "")
    OPEN_ROUTER_MODEL: str = "deepseek/deepseek-r1-0528-qwen3-8b:free"
    OPEN_ROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "Slava_Krutoi")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000
    
    @property
    def database_url(self) -> str:
        return f"postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()

