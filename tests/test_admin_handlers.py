import pytest
from aiogram.filters import Command
from bot.handlers.admin_handlers import (admin_start, write_mailing_message, choose_mailing_list_type, submit_sending,
                                         notify_users)
from bot.fsm import AdminForm
from bot.utils.buttons_factory import create_buttons
from bot.lang_ru import RU_ADMIN_HANDLERS
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_admin_start():
    requester = MockedBot(MessageHandler(admin_start, Command(commands=["admin"])))
    calls = await requester.query(MESSAGE.as_object(text="/admin"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_ADMIN_HANDLERS['hello_admin']

    kb_builder = await create_buttons(["Создать рассылку"])
    expected_reply_markup = kb_builder.as_markup(resize_keyboard=True)
    assert calls.send_message.fetchone().reply_markup == expected_reply_markup


@pytest.mark.asyncio
async def test_write_mailing_message():
    requester = MockedBot(MessageHandler(write_mailing_message, state=AdminForm.mailing_message))
    calls = await requester.query(MESSAGE.as_object(text="создать рассылку"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_ADMIN_HANDLERS['write_mailing_message']


@pytest.mark.asyncio
async def test_choose_mailing_list_type():
    requester = MockedBot(MessageHandler(choose_mailing_list_type, state=AdminForm.choose_sending_type))
    calls = await requester.query(MESSAGE.as_object(text='text'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_ADMIN_HANDLERS['choose_mailing_list_type']

    kb_builder = await create_buttons(['Заполнил профиль', 'Не заполнил профиль', 'Всем'], width=2)
    text = kb_builder.as_markup(resize_keyboard=True).keyboard[0][0].text
    calls = await requester.query(MESSAGE.as_object(text=text))
    assert answer_message == calls.send_message.fetchone().text


@pytest.mark.asyncio
async def test_submit_sending():
    requester = MockedBot(MessageHandler(submit_sending, state=AdminForm.submit_sending))
    kb_builder = await create_buttons(['Заполнил профиль', 'Не заполнил профиль', 'Всем'], width=2)
    text = kb_builder.as_markup(resize_keyboard=True).keyboard[0][0].text
    calls = await requester.query(MESSAGE.as_object(text=text))
    answer_message = calls.send_message.fetchone().text
    data = f'<b>Рассылка адресована тем кто</b>: Заполнил профиль\n\n<b>Сообщение</b>:\n\nДанные не получены'
    assert answer_message == RU_ADMIN_HANDLERS['summary']+data


@pytest.mark.asyncio
async def test_notify_users():
    requester = MockedBot(MessageHandler(notify_users, state=AdminForm.start_sending))
    kb_builder = await create_buttons(['Начать рассылку', 'Отмена'], width=2)
    text = kb_builder.as_markup(resize_keyboard=True).keyboard[0][0].text
    calls = await requester.query(MESSAGE.as_object(text=text))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == 'Пользователей нет, рассылать некому.'