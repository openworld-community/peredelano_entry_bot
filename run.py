import asyncio
import logging
import sys

from hanglers import common_handlers
from dependencies import dp, bot
from utils.misc import check_eventloop_policy

check_eventloop_policy()


async def main():
    dp.include_router(common_handlers.form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
