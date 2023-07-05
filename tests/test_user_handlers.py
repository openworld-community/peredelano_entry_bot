import pytest
from aiogram.filters import Command
from bot.handlers.user_handlers import (command_start, get_role, indicate_experience, choose_tech_stack,
                                        provide_linkedin_link, get_summary_linkedin_not_skipped, finish,
                                        get_summary_linkedin_skipped)
from bot.fsm import UserForm
from bot.utils.buttons_factory import create_buttons
from bot.lang_ru import RU_USER_HANDLERS, RU_USER_HANDLERS_BUTTONS
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_command_start():
    requester = MockedBot(MessageHandler(command_start, Command(commands=["start"])))
    calls = await requester.query(MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_USER_HANDLERS['command_start']

    kb_builder = await create_buttons(["Создать профиль"])
    expected_reply_markup = kb_builder.as_markup(resize_keyboard=True)
    assert calls.send_message.fetchone().reply_markup == expected_reply_markup


@pytest.mark.asyncio
async def test_get_role():
    requester = MockedBot(MessageHandler(get_role, state=UserForm.role))
    calls = await requester.query(MESSAGE.as_object(text="создать профиль"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_USER_HANDLERS['get_specialization']

    kb_builder = await create_buttons(RU_USER_HANDLERS_BUTTONS['roles'], width=3)
    expected_reply_markup = kb_builder.as_markup(resize_keyboard=True)
    assert calls.send_message.fetchone().reply_markup == expected_reply_markup


@pytest.mark.asyncio
async def test_indicate_experience():
    requester = MockedBot(MessageHandler(indicate_experience, state=UserForm.experience))
    kb_builder = await create_buttons(RU_USER_HANDLERS_BUTTONS['roles'], width=3)
    text = kb_builder.as_markup(resize_keyboard=True).keyboard[0][0].text
    calls = await requester.query(MESSAGE.as_object(text=text))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_USER_HANDLERS['check_experience']

    kb_builder = await create_buttons(RU_USER_HANDLERS_BUTTONS['choose_experience'], width=3)
    expected_reply_markup = kb_builder.as_markup(resize_keyboard=True)
    assert calls.send_message.fetchone().reply_markup == expected_reply_markup


@pytest.mark.asyncio
async def test_choose_tech_stack():
    requester = MockedBot(MessageHandler(choose_tech_stack, state=UserForm.tech_stack))
    kb_builder = await create_buttons(RU_USER_HANDLERS_BUTTONS['choose_experience'], width=3)
    text = kb_builder.as_markup(resize_keyboard=True).keyboard[0][0].text
    calls = await requester.query(MESSAGE.as_object(text=text))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_USER_HANDLERS['choose_tech_stack']


@pytest.mark.asyncio
async def test_provide_linkedin_link():
    requester = MockedBot(MessageHandler(provide_linkedin_link, state=UserForm.linkedin_profile))
    calls = await requester.query(MESSAGE.as_object(text='Pandas, Kubernetes, Git, FastAPI'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_USER_HANDLERS['provide_linkedin_link']

    kb_builder = await create_buttons(RU_USER_HANDLERS_BUTTONS['skip_linkedin'], width=1)
    expected_reply_markup = kb_builder.as_markup(resize_keyboard=True)
    assert calls.send_message.fetchone().reply_markup == expected_reply_markup


@pytest.mark.asyncio
async def test_get_summary_linkedin_not_skipped():
    requester = MockedBot(MessageHandler(get_summary_linkedin_not_skipped, state=UserForm.summary))
    calls = await requester.query(MESSAGE.as_object(text='https://www.linkedin.com/in/vasia'))
    answer_message = calls.send_message.fetchone().text
    answer = RU_USER_HANDLERS['summary']
    data = 'Роль: Данные не получены\nОпыт: Данные не получены\n' \
           'Стек: Данные не получены\nLinkedIn: https://www.linkedin.com/in/vasia'
    assert answer_message == answer+data

    kb_builder = await create_buttons(RU_USER_HANDLERS_BUTTONS['finalize_profile'])
    expected_reply_markup = kb_builder.as_markup(resize_keyboard=True)
    assert calls.send_message.fetchone().reply_markup == expected_reply_markup


@pytest.mark.asyncio
async def test_get_summary_linkedin_not_skipped_retry():
    requester = MockedBot(MessageHandler(get_summary_linkedin_not_skipped, state=UserForm.summary))
    calls = await requester.query(MESSAGE.as_object(text='https://www.linkedin.com/'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == RU_USER_HANDLERS['wrong_linkedin_link']

    calls = await requester.query(MESSAGE.as_object(text='https://www.linkedin.com/in/vasia1'))
    answer_message = calls.send_message.fetchone().text
    answer = RU_USER_HANDLERS['summary']
    data = 'Роль: Данные не получены\nОпыт: Данные не получены\n' \
           'Стек: Данные не получены\nLinkedIn: https://www.linkedin.com/in/vasia1'
    assert answer_message == answer + data


@pytest.mark.asyncio
async def test_get_summary_linkedin_skipped():
    requester = MockedBot(MessageHandler(get_summary_linkedin_skipped, state=UserForm.summary))
    calls = await requester.query(MESSAGE.as_object(text='пропустить'))
    answer_message = calls.send_message.fetchone().text
    answer = RU_USER_HANDLERS['summary']
    data = 'Роль: Данные не получены\nОпыт: Данные не получены\n' \
           'Стек: Данные не получены\nLinkedIn: Данные не получены'
    assert answer_message == answer+data

    kb_builder = await create_buttons(RU_USER_HANDLERS_BUTTONS['finalize_profile'])
    expected_reply_markup = kb_builder.as_markup(resize_keyboard=True)
    assert calls.send_message.fetchone().reply_markup == expected_reply_markup

@pytest.mark.asyncio
async def test_finish():
    data = {
        'tg_id': 111,
        'role': 'Backend',
        'experience': '1-3 года',
        'tech_stack': 'Pandas, Kubernetes, Git, FastAPI',
        'linkedin_profile': 'https://www.linkedin.com/in/vasia1',
        'submit': 'Yes',
    }
    requester = MockedBot(MessageHandler(finish, state=UserForm.telegram_link, state_data=data))
    kb_builder = await create_buttons(RU_USER_HANDLERS_BUTTONS['finalize_profile'])
    text = kb_builder.as_markup(resize_keyboard=True).keyboard[0][0].text
    calls = await requester.query(MESSAGE.as_object(text=text))
    answer_message = calls.send_message.fetchall()
    url = answer_message[1].reply_markup['inline_keyboard'][0][0]['url']
    assert answer_message[0].text == 'Спасибо, что заполнил профиль!'
    assert answer_message[1].text == 'Вот ссылка на наш Telegram-канал'
    assert url == 'https://t.me/peredelanoconfjunior'