import pytest
from aiogram.filters import Command
from bot.handlers.other_handlers import cancel_handler
from bot.handlers.user_handlers import command_start
from bot.handlers.admin_handlers import admin_start
from bot.fsm import AdminForm, UserForm
from bot.lang_ru import RU_OTHER_HANDLERS, RU_USER_HANDLERS, RU_ADMIN_HANDLERS
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_cancel_handler_from_user():
    requester = MockedBot(MessageHandler(command_start, Command(commands=["start"])))
    calls = await requester.query(MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_USER_HANDLERS['command_start']

    requester = MockedBot(MessageHandler(cancel_handler, state=UserForm.role))
    calls = await requester.query(MESSAGE.as_object(text="/cancel"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_OTHER_HANDLERS['cancel_handler']


@pytest.mark.asyncio
async def test_cancel_handler_from_admin():
    requester = MockedBot(MessageHandler(admin_start, Command(commands=["admin"])))
    calls = await requester.query(MESSAGE.as_object(text="/admin"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_ADMIN_HANDLERS['hello_admin']

    requester = MockedBot(MessageHandler(cancel_handler, state=AdminForm.mailing_message))
    calls = await requester.query(MESSAGE.as_object(text="/cancel"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_OTHER_HANDLERS['cancel_handler']
