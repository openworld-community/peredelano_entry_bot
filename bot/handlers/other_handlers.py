from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from loguru import logger

from bot.dependencies import other_router
from bot.lang_ru import RU_OTHER_HANDLERS


# ОТМЕНА
@other_router.message(Command("cancel"))
@other_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    logger.info(f"Cancelling state {current_state}")
    await state.clear()
    await message.answer(
        text=RU_OTHER_HANDLERS['cancel_handler'], reply_markup=ReplyKeyboardRemove(remove_keyboard=True), )
