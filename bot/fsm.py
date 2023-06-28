from aiogram.fsm.state import StatesGroup, State


class UserForm(StatesGroup):
    role = State()
    experience = State()
    tech_stack = State()
    linkedin_profile = State()
    summary = State()
    telegram_link = State()


class AdminForm(StatesGroup):
    choose_sending_type = State()
    mailing_message = State()
    submit_sending = State()
    start_sending = State()
