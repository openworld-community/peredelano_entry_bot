from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import DB_TABLE
from dependencies import sb
from utils.misc import calc_total_time, get_datetime, get_userdata


async def upsert_final_data_to_db(state: FSMContext, db_table: str) -> None:
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

    sb.table(db_table).upsert(data, on_conflict='tg_id').execute()


async def collect_initial_data_from_user(message: Message, state: FSMContext) -> None:
    timestamptz, start_time = await get_datetime()
    fullname, tg_id, username = await get_userdata(message)
    await state.update_data(tg_id=tg_id, username=username, fullname=fullname,
                            date=timestamptz, start_time=start_time)
    await upsert_initial_data_to_db(fullname, tg_id, timestamptz, username, DB_TABLE)


async def upsert_initial_data_to_db(fullname, tg_id, timestamptz, username, db_table: str) -> None:
    data = {'tg_id': tg_id, 'username': username, 'fullname': fullname, 'date': timestamptz}
    sb.table(db_table).upsert(data, on_conflict='tg_id').execute()
