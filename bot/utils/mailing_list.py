import asyncio

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import KeyboardBuilder, ButtonType
from loguru import logger

from bot.dependencies import bot
from bot.error_handling.exceptions import BotBlocked
from bot.lang_ru import RU_ADMIN_HANDLERS


async def show_mailing_summary(data: dict, kb_builder: KeyboardBuilder[ButtonType], message) -> None:
    await message.answer(
        text=f'{RU_ADMIN_HANDLERS["summary"]}'
             f'<b>Рассылка адресована тем кто</b>: {data.get("to_whom", "Данные не получены")}\n\n'
             f'<b>Сообщение</b>:\n\n{data.get("mailing_message", "Данные не получены")}',
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


async def select_profiles_for_mailing(completed_profiles, data, uncompleted_profiles):
    if data['to_whom'].lower() == "заполнил профиль":
        return completed_profiles
    elif data['to_whom'].lower() == "не заполнил профиль":
        return uncompleted_profiles
    else:
        return uncompleted_profiles + completed_profiles


async def start_mailing(message_pool, speed, user_ids, data):
    active_users_list = []
    blocked_users_list = []
    for counter, user in enumerate(user_ids, start=1):
        try:
            await bot.send_message(int(user), data['mailing_message'])
            active_users_list.append(user)
        except BotBlocked:
            blocked_users_list.append(user)
            logger.info('Бот был заблокирован пользователем')
        if counter % message_pool == 0 and counter != len(user_ids):
            await asyncio.sleep(speed)
    return active_users_list, blocked_users_list


async def mailing_list_summary(active_users_list: list[str], blocked_users_list: list[str], message: Message,
                               user_ids: list[str]) -> None:
    active_users = len(active_users_list)
    users_who_blocked_bot = len(blocked_users_list)
    pau = active_users * 100 / len(user_ids)
    pbu = users_who_blocked_bot * 100 / len(user_ids)
    await message.answer(f'Рассылка завершена!\n\n'
                         f'Активных пользователей: <b>{active_users}</b> ({round(pau, 2)}%)\n'
                         f'Заблокировавших бота: <b>{users_who_blocked_bot}</b> ({round(pbu, 2)}%)',
                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True), )
