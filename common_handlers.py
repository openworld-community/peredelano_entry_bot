import logging

from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import KeyboardBuilder, ButtonType

from buttons_factory import create_buttons, create_url_button
from dependencies import form_router, sb
from fsm import CommonForm
from lang_ru import RU_COMMON_HANDLERS
from misc import collect_initial_data_from_user


# START
@form_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext) -> None:
    await collect_initial_data_from_user(message, state)
    await state.set_state(CommonForm.role)
    kb_builder: KeyboardBuilder[ButtonType] = await create_buttons(["Создать профиль"])
    await message.answer(text=RU_COMMON_HANDLERS['command_start'],
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
        text=RU_COMMON_HANDLERS['cancel_handler'], reply_markup=ReplyKeyboardRemove(), )


# РОЛЬ
@form_router.message(CommonForm.role, F.text.casefold() == "создать профиль")
async def get_role(message: Message, state: FSMContext) -> None:
    await state.set_state(CommonForm.experience)
    kb_builder: KeyboardBuilder[ButtonType] = await create_buttons(RU_COMMON_HANDLERS['roles'], width=3)
    await message.answer(
        text=RU_COMMON_HANDLERS['get_specialization'],
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


# РОЛЬ ДРУГОЕ
@form_router.message(CommonForm.experience, F.text.casefold() == "другое")
async def get_role_other(message: Message, state: FSMContext) -> None:
    await state.set_state(CommonForm.experience)
    await message.answer('Напиши свою роль', reply_markup=ReplyKeyboardRemove())


# ОПЫТ
@form_router.message(CommonForm.experience)
async def indicate_experience(message: Message, state: FSMContext) -> None:
    await state.set_state(CommonForm.tech_stack)
    await state.update_data(role=message.text)
    kb_builder: KeyboardBuilder[ButtonType] = await create_buttons(["До года", "1-3 года", "3-5 лет",
                                                                    "Свыше 5 лет", "Не работаю"], width=3)
    await message.answer(
        text=RU_COMMON_HANDLERS['check_experience'],
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


# СТЕК
@form_router.message(CommonForm.tech_stack)
async def choose_tech_stack(message: Message, state: FSMContext) -> None:
    await state.set_state(CommonForm.summary)
    await state.update_data(experience=message.text)
    await message.answer(
        text=RU_COMMON_HANDLERS['choose_tech_stack'], reply_markup=ReplyKeyboardRemove(), )


# SUMMARY
@form_router.message(CommonForm.summary)
async def get_summary(message: Message, state: FSMContext) -> None:
    await state.set_state(CommonForm.telegram_link)
    await state.update_data(tech_stack=message.text)
    data: dict[str, str | int] = await state.get_data()
    kb_builder: KeyboardBuilder[ButtonType] = await create_buttons(["Подтвердить", "Отмена"])
    await show_dev_summary(data, kb_builder, message)


async def show_dev_summary(data: dict, kb_builder, message) -> None:
    await message.answer(
        text=f'{RU_COMMON_HANDLERS["summary"]}'

             f'Роль: {data.get("role", "Данные не получены")}\n'
             f'Опыт: {data.get("experience", "Данные не получены")}\n'
             f'Стек: {data.get("tech_stack", "Данные не получены")}',
        reply_markup=kb_builder.as_markup(resize_keyboard=True), )


@form_router.message(CommonForm.telegram_link)
async def finish(message: Message, state: FSMContext) -> None:
    await message.answer('Спасибо, что заполнил профиль!', reply_markup=ReplyKeyboardRemove())
    await state.update_data(submit='yes')

    kb_builder: KeyboardBuilder[ButtonType] = await create_url_button("Peredelano Startups",
                                                                      "https://t.me/peredelanoconfjunior")
    await message.answer("Вот ссылка на наш Telegram-канал",
                         reply_markup=kb_builder.as_markup(resize_keyboard=True), )
    await upsert_final_data_to_db(state)
    await state.clear()


async def upsert_final_data_to_db(state: FSMContext) -> None:
    data: dict[str, int | str] = await state.get_data()
    tg_id = data.get("tg_id", "Данные не получены")
    role = data.get("role", "Данные не получены")
    experience = data.get("experience", "Данные не получены")
    tech_stack = data.get("tech_stack", "Данные не получены")
    submit = data.get("submit", "No")

    data = {"tg_id": tg_id,
            'role': role,
            'experience': experience,
            'tech_stack': tech_stack,
            'submit': submit}

    sb.table('users').upsert(data, on_conflict='tg_id').execute()


@form_router.message()
async def wrong_message(message: Message) -> None:
    await message.reply(text=RU_COMMON_HANDLERS['wrong_answer'])
