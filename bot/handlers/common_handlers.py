import logging

from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.utils.buttons_factory import create_buttons, create_url_button
from config import USERS_TABLE
from bot.db.database import upsert_final_data_to_db, collect_initial_data_from_user
from bot.dependencies import form_router
from bot.fsm import CommonForm
from bot.lang_ru import RU_COMMON_HANDLERS, RU_COMMON_HANDLERS_BUTTONS
from bot.utils.misc import show_dev_summary


# START
@form_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext) -> None:
    await collect_initial_data_from_user(message, state)
    await state.set_state(CommonForm.role)
    kb_builder = await create_buttons(["Создать профиль"])
    await message.answer(text=str(RU_COMMON_HANDLERS['command_start']),
                         reply_markup=kb_builder.as_markup(resize_keyboard=True), )


# ОТМЕНА
@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        text=RU_COMMON_HANDLERS['cancel_handler'], reply_markup=ReplyKeyboardRemove(remove_keyboard=True), )


# РОЛЬ
@form_router.message(CommonForm.role, F.text.casefold() == "создать профиль")
async def get_role(message: Message, state: FSMContext) -> None:
    await state.set_state(CommonForm.experience)
    kb_builder = await create_buttons(RU_COMMON_HANDLERS_BUTTONS['roles'], width=3)
    await message.answer(
        text=RU_COMMON_HANDLERS['get_specialization'],
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


# ОПЫТ
@form_router.message(CommonForm.experience)
async def indicate_experience(message: Message, state: FSMContext) -> None:
    await state.set_state(CommonForm.tech_stack)
    await state.update_data(role=message.text)
    kb_builder = await create_buttons(RU_COMMON_HANDLERS_BUTTONS['choose_experience'], width=3)
    await message.answer(
        text=RU_COMMON_HANDLERS['check_experience'],
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


# СТЕК
@form_router.message(CommonForm.tech_stack, F.text.in_({*RU_COMMON_HANDLERS_BUTTONS['choose_experience']}))
async def choose_tech_stack(message: Message, state: FSMContext) -> None:
    await state.set_state(CommonForm.summary)
    await state.update_data(experience=message.text)
    await message.answer(
        text=RU_COMMON_HANDLERS['choose_tech_stack'], reply_markup=ReplyKeyboardRemove(remove_keyboard=True), )


# SUMMARY
@form_router.message(CommonForm.summary)
async def get_summary(message: Message, state: FSMContext) -> None:
    await state.set_state(CommonForm.telegram_link)
    await state.update_data(tech_stack=message.text)
    data = await state.get_data()
    kb_builder = await create_buttons(["Подтвердить", "Отмена"])
    await show_dev_summary(data, kb_builder, message)


# ССЫЛКА НА КАНАЛ
@form_router.message(CommonForm.telegram_link, F.text.casefold() == "подтвердить")
async def finish(message: Message, state: FSMContext) -> None:
    await message.answer('Спасибо, что заполнил профиль!', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await state.update_data(submit='yes')

    kb_builder = await create_url_button("Peredelano Startups", "https://t.me/peredelanoconfjunior")
    await message.answer("Вот ссылка на наш Telegram-канал",
                         reply_markup=kb_builder.as_markup(resize_keyboard=True), )
    await upsert_final_data_to_db(state, USERS_TABLE)
    await state.clear()


# СООБЩЕНИЕ О НЕПРАВИЛЬНОМ ДЕЙСТВИИ
@form_router.message()
async def wrong_message(message: Message) -> None:
    await message.reply(text=RU_COMMON_HANDLERS['wrong_answer'])
