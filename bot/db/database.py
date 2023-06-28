from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from bot.dependencies import sb
from bot.utils.misc import calc_total_time, get_datetime, get_userdata
from config import USERS_TABLE, MAILING_TABLE


async def upsert_final_data_to_db(state: FSMContext, db_table: str) -> None:
    data: dict[str, int | str | None] = await state.get_data()
    tg_id = data.get("tg_id")
    role = data.get("role")
    experience = data.get("experience")
    tech_stack = data.get("tech_stack")
    linkedin_profile = data.get("linkedin_profile")
    submit = data.get("submit", "No")
    total_time = await calc_total_time(data)

    data = {"tg_id": tg_id,
            'role': role,
            'experience': experience,
            'tech_stack': tech_stack,
            'linkedin_profile': linkedin_profile,
            'submit': submit,
            'total_time_in_sec': total_time}

    sb.table(db_table).upsert(data, on_conflict='tg_id').execute()


async def collect_initial_data_from_user(message: Message, state: FSMContext) -> None:
    timestamptz, start_time = await get_datetime()
    fullname, tg_id, username = await get_userdata(message)
    await state.update_data(tg_id=tg_id, username=username, fullname=fullname,
                            date=timestamptz, start_time=start_time)
    await upsert_initial_data_to_db(fullname, tg_id, timestamptz, username)


async def upsert_initial_data_to_db(fullname: str, tg_id: str, timestamptz, username: str) -> None:
    data = {'tg_id': tg_id, 'username': username, 'fullname': fullname, 'date': timestamptz}
    sb.table(USERS_TABLE).upsert(data, on_conflict='tg_id').execute()


async def get_all_tg_ids() -> tuple[list[str], list[str]]:
    result = sb.table(USERS_TABLE).select("tg_id, submit").execute()
    completed_profiles_tg_ids = []
    uncompleted_profiles_tg_ids = []
    for row in result.data:
        if row['submit'] == 'yes':
            completed_profiles_tg_ids.append(row['tg_id'])
        else:
            uncompleted_profiles_tg_ids.append(row['tg_id'])
    return uncompleted_profiles_tg_ids, completed_profiles_tg_ids


async def insert_mailing_message_to_db(tg_id: str | int, author: str, message: str) -> None:
    data = {'author_tg_id': str(tg_id), 'author': author, 'mailing_message': message}
    sb.table(MAILING_TABLE).insert(data).execute()
    logger.info('Сообщение с текстом рассылки успешно добавлено в базу данных')

