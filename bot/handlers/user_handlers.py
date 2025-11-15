import os
import logging
import aiohttp
import asyncio
import re
from aiogram import Router, F
from aiogram.types import Message
from backend_service import http_service
from aiogram.filters import Command, CommandStart, StateFilter
from keyboards.user_keyboards import RegisterKeyboard, ChooseAssistantKeyboard
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logger = logging.getLogger(__name__)
router = Router()

backend_url = os.getenv("BACKEND_URL", "http://backend:8080")

"""States"""

class AssistantState(StatesGroup):
    question = State()

class RegisterState(StatesGroup):
    name = State()
    surname = State()
    company_name = State()

"""Служебные функции"""

async def create_chats(telegram_id: int) -> bool:
    session = await http_service.get_session()
    for type in range(6):
        try:
            async with session.post(f"{backend_url}/chat/", json={"type": type}, headers={"X-Telegram-User-Id": str(telegram_id)}) as response:
                if response.status == 201:
                    pass
                else:
                    return False
        except Exception as e:
            logger.error(f"Error creating chats: {str(e)}")
            return False
    return True

async def is_registered(telegram_id: int) -> bool:
    session = await http_service.get_session()
    try:
        async with session.get(f"{backend_url}/auth/me", headers={"X-Telegram-User-Id": str(telegram_id)}) as response:
            if response.status == 200:
                return True
            else:
                return False
    except Exception as e:
        logger.error(f"Error checking registration: {str(e)}")
        return False

async def get_chat_id(telegram_id: int, type: int) -> int:
    session = await http_service.get_session()
    try:
        async with session.get(f"{backend_url}/chat/", headers={"X-Telegram-User-Id": str(telegram_id)}) as response:
            if response.status == 200:
                chats = await response.json()
                for chat in chats:
                    if chat["type"] == type:
                        return chat["id"]
            else:
                logger.error(f"Error getting chat id: {response.status}")
                return None
            return None
    except Exception as e:
        logger.error(f"Error getting chat id: {str(e)}")
        return None

def clean_markdown(text: str) -> str:

    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[*_`#]', '', text)
    
    return text.strip()

async def split_long_message(text: str, max_length: int = 4000) -> list[str]:
    if len(text) <= max_length:
        return [text]
    
    parts = []
    paragraphs = text.split('\n\n')
    current_part = ""
    
    for paragraph in paragraphs:
        if len(paragraph) > max_length:
            if current_part:
                parts.append(current_part.strip())
                current_part = ""
            lines = paragraph.split('\n')
            for line in lines:
                if len(current_part) + len(line) + 1 <= max_length:
                    if current_part:
                        current_part += "\n" + line
                    else:
                        current_part = line
                else:
                    if current_part:
                        parts.append(current_part.strip())
                    current_part = line
        else:
            separator = "\n\n" if current_part else ""
            if len(current_part) + len(paragraph) + len(separator) <= max_length:
                current_part += separator + paragraph
            else:
                if current_part:
                    parts.append(current_part.strip())
                current_part = paragraph
    
    if current_part:
        parts.append(current_part.strip())
    
    return parts

async def send_long_message(message: Message, text: str, reply_markup=None, delay: float = 0.3):
    parts = await split_long_message(text)
    
    for i, part in enumerate(parts):
        markup = reply_markup if i == 0 else None
        await message.answer(part, reply_markup=markup)
        
        if i < len(parts) - 1:
            await asyncio.sleep(delay)

    

"""Basic commands"""

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот-помощник для малого бизнеса. Я могу помочь тебе с различными вопросами, связанными с ведением бизнеса. Чтобы начать работу, используй команду /help или кнопки ниже")
    telegram_id = message.from_user.id
    if not await is_registered(telegram_id):
        await message.answer("Предлагаю пройти регистрацию, чтобы я мог лучше тебе помочь", reply_markup=RegisterKeyboard)
    else:
        await message.answer("Вы можете выбрать одного из помощников и задать ему вопрос", reply_markup=ChooseAssistantKeyboard)


@router.message(Command("help"))
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
    telegram_id = message.from_user.id
    data = await state.get_data()
    data["telegram_id"] = telegram_id
    session = await http_service.get_session()
    try:
        async with session.post(f"{backend_url}/auth/register", json=data) as response:
            if response.status == 201:
                await message.answer("Вы успешно зарегистрированы", reply_markup=ChooseAssistantKeyboard)
                # генерация чатов
                await create_chats(telegram_id)
            else:
                await message.answer("Произошла ошибка при регистрации. Попробуйте позже.")
                logger.error(f"Error registering user: {response.status}")
    except Exception as e:
        await message.answer("Произошла ошибка при регистрации. Попробуйте позже.")
        logger.error(f"Error registering user: {str(e)}")
    await state.clear()

"""Assistants"""

@router.message(F.text == "Юридический помощник")
async def legal_assistant(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if not await is_registered(telegram_id):
        await message.answer("Вы не зарегистрированы", reply_markup=RegisterKeyboard)
        return
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=0)
    await message.answer("Вы выбрали Юридический помощник. Задайте свой вопрос", reply_markup=ReplyKeyboardRemove())

@router.message(F.text == "Маркетинговый помощник")
async def marketing_assistant(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if not await is_registered(telegram_id):
        await message.answer("Вы не зарегистрированы", reply_markup=RegisterKeyboard)
        return
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=1)
    await message.answer("Вы выбрали Маркетинговый помощник. Задайте свой вопрос", reply_markup=ReplyKeyboardRemove())

@router.message(F.text == "Финансовый помощник")
async def financial_assistant(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if not await is_registered(telegram_id):
        await message.answer("Вы не зарегистрированы", reply_markup=RegisterKeyboard)
        return
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=2)
    await message.answer("Вы выбрали Финансовый помощник. Задайте свой вопрос", reply_markup=ReplyKeyboardRemove())

@router.message(F.text == "HR помощник")
async def hr_assistant(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if not await is_registered(telegram_id):
        await message.answer("Вы не зарегистрированы", reply_markup=RegisterKeyboard)
        return
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=3)
    await message.answer("Вы выбрали HR помощник. Задайте свой вопрос", reply_markup=ReplyKeyboardRemove())

@router.message(F.text == "Помощник по подсказкам и напоминаниям")
async def reminder_assistant(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if not await is_registered(telegram_id):
        await message.answer("Вы не зарегистрированы", reply_markup=RegisterKeyboard)
        return
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=4)
    await message.answer("Вы выбрали помощника по подсказкам. Задайте свой вопрос", reply_markup=ReplyKeyboardRemove())

@router.message(F.text == "Гайд-помощник")
async def guide_assistant(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if not await is_registered(telegram_id):
        await message.answer("Вы не зарегистрированы", reply_markup=RegisterKeyboard)
        return
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=5)
    await message.answer("Вы выбрали гайд-помощник. Задайте свой вопрос", reply_markup=ReplyKeyboardRemove())

"""Assistant main handler"""

@router.message(AssistantState.question)
async def process_question(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    telegram_id = message.from_user.id
    chat_id = await get_chat_id(telegram_id, data["chat_type"])
    data["chat_id"] = chat_id
    session = await http_service.get_session()
    start_message = await message.answer("Генерирую ответ...")
    # await message.answer(f"{data}")
    try:
        async with session.post(f"{backend_url}/chat/message", headers={"X-Telegram-User-Id": str(telegram_id)}, json=data) as response:
            if response.status == 200:
                answer = await response.json()
                text = answer["text"]
                # Удаляем Markdown разметку
                text = clean_markdown(text)
                await send_long_message(message, text, reply_markup=ChooseAssistantKeyboard)
                await start_message.delete()
            else:
                await message.answer("Произошла ошибка при отправке вопроса. Попробуйте позже.", reply_markup=ChooseAssistantKeyboard)
                logger.error(f"Error sending question: {response.status}")
    except Exception as e:
        await message.answer("Произошла ошибка при отправке вопроса. Попробуйте позже.", reply_markup=ChooseAssistantKeyboard)
        logger.error(f"Error sending question: {str(e)}")
    await state.clear()
    
