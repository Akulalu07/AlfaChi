from aiogram.fsm.state import State, StatesGroup


class AssistantState(StatesGroup):
    question = State()

class RegisterState(StatesGroup):
    user_name = State()
    company_name = State()
    company_info = State()
