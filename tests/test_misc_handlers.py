import pytest
from bot.handlers.misc_handlers import wrong_message
from bot.lang_ru import RU_MISC_HANDLERS
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE, MESSAGE_WITH_AUDIO, MESSAGE_WITH_CONTACT, MESSAGE_WITH_DOCUMENT, MESSAGE_WITH_LOCATION


@pytest.mark.asyncio
async def test_wrong_message_from_command():
    requester = MockedBot(MessageHandler(wrong_message))
    calls = await requester.query(MESSAGE.as_object(text="/wrong"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_MISC_HANDLERS['wrong_answer']


@pytest.mark.asyncio
async def test_wrong_message_from_text():
    requester = MockedBot(MessageHandler(wrong_message))
    calls = await requester.query(MESSAGE.as_object(text="Hello BOT!"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_MISC_HANDLERS['wrong_answer']


@pytest.mark.asyncio
async def test_wrong_message():
    requester = MockedBot(MessageHandler(wrong_message))
    calls = await requester.query(MESSAGE_WITH_AUDIO.as_object())
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_MISC_HANDLERS['wrong_answer']

    calls = await requester.query(MESSAGE_WITH_CONTACT.as_object())
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_MISC_HANDLERS['wrong_answer']

    calls = await requester.query(MESSAGE_WITH_DOCUMENT.as_object())
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_MISC_HANDLERS['wrong_answer']

    calls = await requester.query(MESSAGE_WITH_LOCATION.as_object())
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_MISC_HANDLERS['wrong_answer']