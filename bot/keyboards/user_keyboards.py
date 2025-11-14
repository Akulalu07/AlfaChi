from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

RegisterKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация")]
    ],
    resize_keyboard=True
)