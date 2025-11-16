from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from stuff import *

from .assistants import router as assistants
from .auth import router as auth


router = Router()
router.include_router(auth)
router.include_router(assistants)


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(t["help"])
