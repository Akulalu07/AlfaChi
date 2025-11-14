import os
import logging
import aiohttp
from aiogram import Router, F
from aiogram.types import Message
from backend_service import http_service
from aiogram.filters import Command, CommandStart, CommandHelp, StateFilter
from keyboards.user_keyboards import RegisterKeyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logger = logging.getLogger(__name__)
router = Router()

backend_url = os.getenv("BACKEND_URL", "http://backend:8080")

class RegisterState(StatesGroup):
    name = State()
    surname = State()
    company_name = State()


"""Basic commands"""

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот-помощник для малого бизнеса. Я могу помочь тебе с различными вопросами, связанными с ведением бизнеса. Чтобы начать работу, используй команду /help или кнопки ниже")
    await message.answer("Предлагаю пройти регистрацию, чтобы я мог лучше тебе помочь", reply_markup=RegisterKeyboard)

@router.message(CommandHelp())
async def help_command(message: Message):
    await message.answer(f"Доступные команды: \n/help - помощь\n/register - регистрация\n/update - обновление данных")

"""Profile commands"""

@router.message(F.text == "Регистрация")
@router.message(Command("register"))
async def register_command(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    session = await http_service.get_session()

    try:
        async with session.get(f"{backend_url}/auth/me", headers={"X-Telegram-User-Id": str(telegram_id)}) as response:
            if response.status == 200:
                await message.answer("Вы уже зарегистрированы!")
            else:
                await message.answer("Пожалуйста, введите ваше имя")
                await state.set_state(RegisterState.name)
    except Exception as e:
        await message.answer("Произошла ошибка при проверке регистрации. Попробуйте позже.")
        logger.error(f"Error checking registration: {str(e)}")

@router.message(RegisterState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Пожалуйста, введите вашу фамилию")
    await state.set_state(RegisterState.surname)

@router.message(RegisterState.surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Пожалуйста, введите вашу компанию")
    await state.set_state(RegisterState.company_name)

@router.message(RegisterState.company_name)
async def process_company_name(message: Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    await message.answer("Поздравляю! Вы успешно зарегистрированы")
    data = await state.get_data()
    await state.clear()
