from aiogram.fsm.state import StatesGroup, State


class CommonForm(StatesGroup):
    create_profile = State()
    role = State()
    other_role = State()
    experience = State()
    tech_stack = State()
    summary = State()
    telegram_link = State()