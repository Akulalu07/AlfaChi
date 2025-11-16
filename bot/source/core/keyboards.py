from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from stuff import *


RegisterKeyboard = ReplyKeyboardMarkup (
    keyboard = [ [ KeyboardButton(text=t["keyboard.register"]) ] ],
    resize_keyboard=True,
)


AssistantKeyboard = ReplyKeyboardMarkup (
    keyboard = [
        [ KeyboardButton(text=t["keyboard.legal_assistant"]),     KeyboardButton(text=t["keyboard.marketing_assistant"]) ],
        [ KeyboardButton(text=t["keyboard.financial_assistant"]), KeyboardButton(text=t["keyboard.hr_assistant"])        ],
        [ KeyboardButton(text=t["keyboard.reminder_assistant"]),  KeyboardButton(text=t["keyboard.guide_assistant"])     ],
    ],
    resize_keyboard = True,
)
