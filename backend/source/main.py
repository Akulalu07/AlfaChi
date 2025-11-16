from fastapi import FastAPI

from contextlib import asynccontextmanager
from database import Database

from auth.router import router as auth_router
from chat.router import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Функции до старта приложения
    await Database.init()
    yield
    # Когда приложение завершает работу
    await Database.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(chat_router)
