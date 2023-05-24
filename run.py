import asyncio
import logging
import sys

import common_handlers
from dependencies import dp, bot

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())




async def main():
    # Регистриуем роутеры в диспетчере
    # dp.include_router(dev_handlers.dev_router)
    dp.include_router(common_handlers.form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
