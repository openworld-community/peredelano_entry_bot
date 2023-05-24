import asyncio
import sys
from datetime import datetime

import pytz
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from dependencies import sb


def check_eventloop_policy():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def upsert_userdata(col: str, val: str) -> None:
    data = {col: val}
    sb.table('users').upsert(data, on_conflict='tg_id').execute()


async def collect_initial_data_from_user(message: Message, state: FSMContext) -> None:
    timestamptz = await get_timstamptz()
    fullname, tg_id, username = await get_userdata(message)
    await state.update_data(tg_id=tg_id, username=username, fullname=fullname, date=timestamptz)
    await upsert_initial_data_to_db(fullname, tg_id, timestamptz, username)


async def upsert_initial_data_to_db(fullname, tg_id, timestamptz, username):
    data = {'tg_id': tg_id, 'username': username, 'fullname': fullname, 'date': timestamptz}
    sb.table('users').upsert(data, on_conflict='tg_id').execute()


async def get_userdata(message):
    tg_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name
    return fullname, tg_id, username


async def get_timstamptz():
    now = datetime.now()
    timestamptz = now.astimezone(pytz.timezone('UTC'))
    timestamptz = timestamptz.strftime("%Y-%m-%d %H:%M:%S %Z")
    return timestamptz


def check_string(input_string):
    return True
