from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from stuff import *

from ..keyboards import *
from ..states import *
from ..utils import *


router = Router()


@router.message(Command("start"))
async def start_command(message: Message) -> None:
    await message.answer(t["start.greeting"])
    telegram_id: int = message.from_user.id

    if not await is_registered(telegram_id):
        await message.answer(t["start.register"], reply_markup=RegisterKeyboard)
    else:
        await message.answer(t["start.continue"], reply_markup=AssistantKeyboard)


@router.message(F.text == t["keyboard.register"])
@router.message(Command("register"))
async def register_command(message: Message, state: FSMContext) -> None:
    telegram_id: int = message.from_user.id

    try:
        async with (await backend.get(f"/auth/me", headers={"X-Telegram-User-Id": str(telegram_id)})) as response:
            if response.status == 200:
                await message.answer(t["register.already_done"])
            else:
                await message.answer(t["register.enter_name"])
                await state.set_state(RegisterState.name)

    except Exception as error:
        logger.error(f"Error checking registration: {str(error)}")
        await message.answer(t["register.check_error"])


@router.message(RegisterState.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(t["register.enter_surname"])
    await state.set_state(RegisterState.surname)


@router.message(RegisterState.surname)
async def process_surname(message: Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    await message.answer(t["register.enter_company"])
    await state.set_state(RegisterState.company_name)


@router.message(RegisterState.company_name)
async def process_company_name(message: Message, state: FSMContext) -> None:
    await state.update_data(company_name=message.text)

    data = await state.get_data()
    telegram_id: int = message.from_user.id
    data["telegram_id"] = telegram_id

    try:
        async with (await backend.post("/auth/register", json=data)) as response:
            if response.status == 201:
                await message.answer(t["register.success"], reply_markup=AssistantKeyboard)
                await create_chats(telegram_id)
            else:
                logger.error(f"Error registering user: {response.status}")
                await message.answer(t["register.register_error"])

    except Exception as error:
        logger.error(f"Error registering user: {str(error)}")
        await message.answer(t["register.register_error"])

    await state.clear()
