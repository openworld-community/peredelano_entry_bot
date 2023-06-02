from aiogram.fsm.state import StatesGroup, State


class CommonForm(StatesGroup):
    role = State()
    experience = State()
    tech_stack = State()
    summary = State()
    telegram_link = State()


class Admin(StatesGroup):
    choose_sending_type = State()
    mailing_message = State()
    submit_sending = State()
    start_sending = State()
