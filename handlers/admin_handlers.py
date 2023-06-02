from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import config
from db.database import get_all_tg_ids, insert_mailing_message_to_db
from dependencies import admin_router
from fsm import Admin
from lang_ru import RU_ADMIN_HANDLERS
from utils.buttons_factory import create_buttons
from utils.mailing_list import select_profiles_for_mailing, start_mailing, mailing_list_summary, \
    show_mailing_summary


# ADMIN START
@admin_router.message(Command("admin"), F.from_user.id.in_({*config.tg_bot.admins_list}))
async def admin_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Admin.mailing_message)
    kb_builder = await create_buttons(["Создать рассылку"])
    await message.answer(text=RU_ADMIN_HANDLERS['hello_admin'],
                         reply_markup=kb_builder.as_markup(resize_keyboard=True), )


# WRITE MAILING MESSAGE
@admin_router.message(Admin.mailing_message, F.text.casefold() == "создать рассылку",
                      F.from_user.id.in_({*config.tg_bot.admins_list}))
async def choose_mailing_list_type(message: Message, state: FSMContext) -> None:
    await state.set_state(Admin.choose_sending_type)
    await message.answer(
        text=RU_ADMIN_HANDLERS['write_mailing_message'],
        reply_markup=ReplyKeyboardRemove(), )


# CREATE MAILING LIST
@admin_router.message(Admin.choose_sending_type, F.from_user.id.in_({*config.tg_bot.admins_list}))
async def choose_mailing_list_type(message: Message, state: FSMContext) -> None:
    await state.set_state(Admin.submit_sending)
    await state.update_data(mailing_message=message.text)
    kb_builder = await create_buttons(['Заполнил профиль', 'Не заполнил профиль', 'Всем'], width=2)
    await message.answer(
        text=RU_ADMIN_HANDLERS['choose_mailing_list_type'],
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


# SUBMIT MAILING LIST
@admin_router.message(Admin.submit_sending, F.text.casefold() == "заполнил профиль",
                      F.from_user.id.in_({*config.tg_bot.admins_list}))
@admin_router.message(Admin.submit_sending, F.text.casefold() == "не заполнил профиль",
                      F.from_user.id.in_({*config.tg_bot.admins_list}))
@admin_router.message(Admin.submit_sending, F.text.casefold() == "всем",
                      F.from_user.id.in_({*config.tg_bot.admins_list}))
async def submit_sending(message: Message, state: FSMContext) -> None:
    await state.set_state(Admin.start_sending)
    await state.update_data(to_whom=message.text)
    data = await state.get_data()
    kb_builder = await create_buttons(['Начать рассылку', 'Отмена'], width=2)
    await show_mailing_summary(data, kb_builder, message)


@admin_router.message(Admin.start_sending, F.text.casefold() == "начать рассылку",
                      F.from_user.id.in_({*config.tg_bot.admins_list}))
async def notify_users(message: Message, state: FSMContext):
    message_pool = 10
    time_gap = 1  # Time gap between message pools

    uncompleted_profiles, completed_profiles = await get_all_tg_ids()

    if uncompleted_profiles + completed_profiles == []:
        await state.clear()
        return await message.answer('Пользователей нет, рассылать некому.', reply_markup=ReplyKeyboardRemove())

    await message.answer(
        text=RU_ADMIN_HANDLERS['mailing_has_started'],
        reply_markup=ReplyKeyboardRemove(), )

    data = await state.get_data()
    author_tg_id, author, mailing_message = message.from_user.id, message.from_user.full_name, data['mailing_message']

    await insert_mailing_message_to_db(author_tg_id, author, mailing_message)

    user_ids = await select_profiles_for_mailing(completed_profiles, data, uncompleted_profiles)

    active_users_list, blocked_users_list = await start_mailing(message_pool, time_gap, user_ids, data)

    await mailing_list_summary(active_users_list, blocked_users_list, message, user_ids)
    await state.clear()
