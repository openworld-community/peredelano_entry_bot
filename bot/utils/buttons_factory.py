from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardBuilder, InlineKeyboardBuilder


async def create_buttons(btn_names: list, width: int = 2) -> KeyboardBuilder[KeyboardButton]:
    kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [KeyboardButton(text=i) for i in btn_names]
    return kb_builder.row(*buttons, width=width)


async def create_inline_buttons(btn_names: list[str], callbacks: list[str], width: int = 1):
    inline_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    inline_buttons: list[InlineKeyboardButton] = \
        [InlineKeyboardButton(text=i, callback_data=j) for i, j in zip(btn_names, callbacks)]
    return inline_builder.row(*inline_buttons, width=width)


async def create_url_button(btn_name: str, url: str):
    url_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    url_button: InlineKeyboardButton = InlineKeyboardButton(text=btn_name, url=url)
    return url_builder.row(url_button, width=1)
