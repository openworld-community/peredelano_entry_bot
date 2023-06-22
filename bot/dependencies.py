from aiogram import Router, Bot, Dispatcher
from supabase import Client, create_client

from config import config

other_router: Router = Router()
user_router: Router = Router()
admin_router: Router = Router()
misc_router: Router = Router()


bot: Bot = Bot(token=config.tg_bot.bot_token, parse_mode="HTML")

dp: Dispatcher = Dispatcher()

sb: Client = create_client(config.tg_bot.supabase_url, config.tg_bot.supabase_key)
