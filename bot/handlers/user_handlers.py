import logging

from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.utils.buttons_factory import create_buttons, create_url_button
from config import USERS_TABLE
from bot.db.database import upsert_final_data_to_db, collect_initial_data_from_user
from bot.dependencies import user_router
from bot.fsm import UserForm
from bot.lang_ru import RU_USER_HANDLERS, RU_COMMON_HANDLERS_BUTTONS
from bot.utils.misc import show_dev_summary


# START
@user_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext) -> None:
    await collect_initial_data_from_user(message, state)
    await state.set_state(UserForm.role)
    kb_builder = await create_buttons(["Создать профиль"])
    await message.answer(text=str(RU_USER_HANDLERS['command_start']),
                         reply_markup=kb_builder.as_markup(resize_keyboard=True), )


# ROLES
@user_router.message(UserForm.role, F.text.casefold() == "создать профиль")
async def get_role(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.experience)
    kb_builder = await create_buttons(RU_COMMON_HANDLERS_BUTTONS['roles'], width=3)
    await message.answer(
        text=RU_USER_HANDLERS['get_specialization'],
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


# EXPERIENCE
@user_router.message(UserForm.experience, F.text)
async def indicate_experience(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.tech_stack)
    await state.update_data(role=message.text)
    kb_builder = await create_buttons(RU_COMMON_HANDLERS_BUTTONS['choose_experience'], width=3)
    await message.answer(
        text=RU_USER_HANDLERS['check_experience'],
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


# STACK
@user_router.message(UserForm.tech_stack, F.text.in_({*RU_COMMON_HANDLERS_BUTTONS['choose_experience']}))
async def choose_tech_stack(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.summary)
    await state.update_data(experience=message.text)
    await message.answer(
        text=RU_USER_HANDLERS['choose_tech_stack'], reply_markup=ReplyKeyboardRemove(remove_keyboard=True), )


# SUMMARY
@user_router.message(UserForm.summary, F.text)
async def get_summary(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.telegram_link)
    await state.update_data(tech_stack=message.text)
    data = await state.get_data()
    kb_builder = await create_buttons(["Подтвердить", "Отмена"])
    await show_dev_summary(data, kb_builder, message)


# LINK TO TELEGRAM GROUP
@user_router.message(UserForm.telegram_link, F.text.casefold() == "подтвердить")
async def finish(message: Message, state: FSMContext) -> None:
    await message.answer('Спасибо, что заполнил профиль!', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await state.update_data(submit='yes')

    kb_builder = await create_url_button("Peredelano Community", "https://t.me/peredelanoconfjunior")
    await message.answer("Нажимай на кнопку чтобы присоединиться к нашей группе.",
                         reply_markup=kb_builder.as_markup(resize_keyboard=True), )
    await upsert_final_data_to_db(state, USERS_TABLE)
    await state.clear()
