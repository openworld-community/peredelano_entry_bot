import asyncio
import re
import sys
import time
from datetime import datetime

import pytz
from aiogram.utils.keyboard import KeyboardBuilder, ButtonType

from bot.lang_ru import RU_USER_HANDLERS


def check_eventloop_policy() -> None:
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def show_dev_summary(data: dict, kb_builder: KeyboardBuilder[ButtonType], message) -> None:
    display_linkedin = data.get("linkedin_profile")
    await message.answer(
        text=f'{RU_USER_HANDLERS["summary"]}'

             f'Роль: {data.get("role", "Данные не получены")}\n'
             f'Опыт: {data.get("experience", "Данные не получены")}\n'
             f'Стек: {data.get("tech_stack", "Данные не получены")}\n'
             f'LinkedIn: {display_linkedin if display_linkedin else "Данные не получены" }',
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


async def get_linkedin_link(link: str):
    pattern = "^https://(www.)?linkedin.com/.+$"
    return link if re.match(pattern, link) else None


def check_string(input_string):
    return True
