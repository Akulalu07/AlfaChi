from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

RegisterKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация")]
    ],
    resize_keyboard=True
)

ChooseAssistantKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Юридический помощник"), KeyboardButton(text="Маркетинговый помощник")],
        [KeyboardButton(text="Финансовый помощник"), KeyboardButton(text="HR помощник")],
        [KeyboardButton(text="Помощник по подсказкам и напоминаниям"), KeyboardButton(text="Гайд-помощник")]
    ],
    resize_keyboard = True
)