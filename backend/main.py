from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db, close_db
from auth.router import router as auth_router
from chat.router import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Функции до старта приложения
    await init_db()
    yield
    # Когда приложение завершает работу
    await close_db()

app = FastAPI(lifespan=lifespan, title="Goooyda")

app.include_router(auth_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "Goooyda"}