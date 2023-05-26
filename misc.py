import asyncio
import sys
import time
from datetime import datetime

import pytz
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import KeyboardBuilder, ButtonType

from dependencies import sb
from lang_ru import RU_COMMON_HANDLERS


def check_eventloop_policy():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def show_dev_summary(data: dict, kb_builder: KeyboardBuilder[ButtonType], message) -> None:
    await message.answer(
        text=f'{RU_COMMON_HANDLERS["summary"]}'

             f'Роль: {data.get("role", "Данные не получены")}\n'
             f'Опыт: {data.get("experience", "Данные не получены")}\n'
             f'Стек: {data.get("tech_stack", "Данные не получены")}',
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


async def calc_total_time(data: dict) -> int:
    start_time = data.get("start_time", 0)
    end_time = int(time.time())
    return end_time - start_time


async def upsert_final_data_to_db(state: FSMContext) -> None:
    data: dict[str, int | str] = await state.get_data()
    tg_id = data.get("tg_id", "Данные не получены")
    role = data.get("role", "Данные не получены")
    experience = data.get("experience", "Данные не получены")
    tech_stack = data.get("tech_stack", "Данные не получены")
    submit = data.get("submit", "No")
    total_time = await calc_total_time(data)

    data = {"tg_id": tg_id,
            'role': role,
            'experience': experience,
            'tech_stack': tech_stack,
            'submit': submit,
            'total_time_in_sec': total_time}

    sb.table('users').upsert(data, on_conflict='tg_id').execute()


async def upsert_userdata(col: str, val: str) -> None:
    data = {col: val}
    sb.table('users').upsert(data, on_conflict='tg_id').execute()


async def collect_initial_data_from_user(message: Message, state: FSMContext) -> None:
    timestamptz, start_time = await get_datetime()
    fullname, tg_id, username = await get_userdata(message)
    await state.update_data(tg_id=tg_id, username=username, fullname=fullname,
                            date=timestamptz, start_time=start_time)
    await upsert_initial_data_to_db(fullname, tg_id, timestamptz, username)


async def upsert_initial_data_to_db(fullname, tg_id, timestamptz, username):
    data = {'tg_id': tg_id, 'username': username, 'fullname': fullname, 'date': timestamptz}
    sb.table('users').upsert(data, on_conflict='tg_id').execute()


async def get_userdata(message):
    tg_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name
    return fullname, tg_id, username


async def get_datetime():
    now = datetime.now()
    timestamptz = now.astimezone(pytz.timezone('UTC'))
    timestamptz = timestamptz.strftime("%Y-%m-%d %H:%M:%S %Z")
    start_time = int(time.time())
    return timestamptz, start_time


def check_string(input_string):
    return True
