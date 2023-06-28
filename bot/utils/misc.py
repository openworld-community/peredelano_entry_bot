import asyncio
import re
import sys
import time
from datetime import datetime

import pytz
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import KeyboardBuilder, ButtonType

from bot.fsm import UserForm
from bot.lang_ru import RU_USER_HANDLERS, RU_COMMON_HANDLERS_BUTTONS
from bot.utils.buttons_factory import create_buttons


def check_eventloop_policy() -> None:
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def show_dev_summary(data: dict, kb_builder: KeyboardBuilder[ButtonType], message) -> None:
    await message.answer(
        text=f'{RU_USER_HANDLERS["summary"]}'
             f'Роль: {data.get("role", "Данные не получены")}\n'
             f'Опыт: {data.get("experience", "Данные не получены")}\n'
             f'Стек: {data.get("tech_stack", "Данные не получены")}\n'
             f'LinkedIn: {data.get("linkedin_profile", "Данные не получены")}',
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


async def calc_total_time(data: dict) -> int:
    start_time = data.get("start_time", 0)
    end_time = int(time.time())
    return end_time - start_time


async def get_userdata(message) -> tuple[str, str, str]:
    tg_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name
    return fullname, tg_id, username


async def get_datetime() -> tuple[str, int]:
    now = datetime.now()
    timestamptz = now.astimezone(pytz.timezone('UTC'))
    formatted_timestamptz = timestamptz.strftime("%Y-%m-%d %H:%M:%S %Z")
    start_time = int(time.time())
    return formatted_timestamptz, start_time


async def check_linkedin_link(message: str) -> bool:
    pattern = re.compile(r'^https://(www.)?linkedin.com/.+$')
    return True if re.match(pattern, message) else False


async def finalize_profile(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.telegram_link)
    data = await state.get_data()
    kb_builder = await create_buttons(RU_COMMON_HANDLERS_BUTTONS['finalize_profile'])
    await show_dev_summary(data, kb_builder, message)
