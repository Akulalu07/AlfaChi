from aiogram.fsm.state import State, StatesGroup


class AssistantState(StatesGroup):
    question = State()

class RegisterState(StatesGroup):
    name = State()
    surname = State()
    company_name = State()
