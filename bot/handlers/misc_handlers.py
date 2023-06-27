from aiogram.types import Message

from bot.dependencies import misc_router
from bot.lang_ru import RU_MISC_HANDLERS


# СООБЩЕНИЕ О НЕПРАВИЛЬНОМ ДЕЙСТВИИ
@misc_router.message()
async def wrong_message(message: Message) -> None:
    await message.reply(text=RU_MISC_HANDLERS['wrong_answer'])
