from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from stuff import *

from ..keyboards import *
from ..states import *
from ..utils import *


router = Router()


@router.message(F.text == t["keyboard.legal_assistant"])
async def legal_assistant(message: Message, state: FSMContext) -> None:
    telegram_id: int = message.from_user.id

    if not await is_registered(telegram_id):
        await message.answer(t["register.not_registered"], reply_markup=RegisterKeyboard)
        return
    
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=0)
    await message.answer(t["assistant.prompt_legal"], reply_markup=ReplyKeyboardRemove())


@router.message(F.text == t["keyboard.marketing_assistant"])
async def marketing_assistant(message: Message, state: FSMContext):
    telegram_id: int = message.from_user.id

    if not await is_registered(telegram_id):
        await message.answer(t["register.not_registered"], reply_markup=RegisterKeyboard)
        return
    
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=1)
    await message.answer(t["assistant.prompt_marketing"], reply_markup=ReplyKeyboardRemove())


@router.message(F.text == t["keyboard.financial_assistant"])
async def financial_assistant(message: Message, state: FSMContext):
    telegram_id: int = message.from_user.id

    if not await is_registered(telegram_id):
        await message.answer(t["register.not_registered"], reply_markup=RegisterKeyboard)
        return
    
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=2)
    await message.answer(t["assistant.prompt_financial"], reply_markup=ReplyKeyboardRemove())


@router.message(F.text == t["keyboard.hr_assistant"])
async def hr_assistant(message: Message, state: FSMContext):
    telegram_id: int = message.from_user.id

    if not await is_registered(telegram_id):
        await message.answer(t["register.not_registered"], reply_markup=RegisterKeyboard)
        return
    
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=3)
    await message.answer(t["assistant.prompt_hr"], reply_markup=ReplyKeyboardRemove())


@router.message(F.text == t["keyboard.reminder_assistant"])
async def reminder_assistant(message: Message, state: FSMContext):
    telegram_id: int = message.from_user.id

    if not await is_registered(telegram_id):
        await message.answer(t["register.not_registered"], reply_markup=RegisterKeyboard)
        return
    
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=4)
    await message.answer(t["assistant.prompt_reminder"], reply_markup=ReplyKeyboardRemove())


@router.message(F.text == t["keyboard.guide_assistant"])
async def guide_assistant(message: Message, state: FSMContext):
    telegram_id: int = message.from_user.id

    if not await is_registered(telegram_id):
        await message.answer(t["register.not_registered"], reply_markup=RegisterKeyboard)
        return
    
    await state.set_state(AssistantState.question)
    await state.update_data(chat_type=5)
    await message.answer(t["assistant.prompt_guide"], reply_markup=ReplyKeyboardRemove())


@router.message(AssistantState.question)
async def process_question(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)

    data = await state.get_data()
    telegram_id = message.from_user.id
    chat_id = await get_chat_id(telegram_id, data["chat_type"])
    data["chat_id"] = chat_id
    start_message = await message.answer(t["assistant.generating"])

    try:
        async with (await backend.post("/chats/messages", headers={"X-Telegram-User-Id": str(telegram_id)}, json=data)) as response:
            if response.status == 200:
                answer = await response.json()
                text = answer["text"]
                text = clean_markdown(text)
                await send_long_message(message, text, reply_markup=AssistantKeyboard)
                await start_message.delete()

            else:
                logger.error(f"Error sending question: {response.status}")
                await message.answer(t["backend.send_error"], reply_markup=AssistantKeyboard)

    except Exception as error:
        logger.error(f"Error sending question: {str(error)}")
        await message.answer(t["backend.send_error"], reply_markup=AssistantKeyboard)

    await state.clear()
