import asyncio
from bot.handlers import admin_handlers
from bot.handlers import user_handlers
from bot.handlers import other_handlers
from bot.handlers import misc_handlers
from bot.dependencies import dp, bot
from bot.utils.misc import check_eventloop_policy

check_eventloop_policy()


async def main():
    dp.include_router(other_handlers.other_router)
    dp.include_router(user_handlers.user_router)
    dp.include_router(admin_handlers.admin_router)
    dp.include_router(misc_handlers.misc_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
