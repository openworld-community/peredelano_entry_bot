import asyncio
import re
import sys
import time
from datetime import datetime, timedelta

import pytz
from aiogram.dispatcher.dispatcher import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import KeyboardBuilder, ButtonType

from bot.dependencies import bot
from bot.fsm import UserForm
from bot.lang_ru import RU_USER_HANDLERS, RU_USER_HANDLERS_BUTTONS
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
    kb_builder = await create_buttons(RU_USER_HANDLERS_BUTTONS['finalize_profile'])
    await show_dev_summary(data, kb_builder, message)


async def check_storage_old(storage: MemoryStorage):
    current_time, _ = await get_datetime()

    for key, value in storage.storage.items():
        date_str = value.data.get('date')
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %Z')
            time_difference = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S %Z') - date
            if time_difference >= timedelta(days=7):
                await storage.set_data(bot=bot, key=key, data={'data': {}})
                await storage.set_state(bot=bot, key=key, state=None)
