from dataclasses import dataclass

from environs import Env

PROJECT_STATUS = 'prod'


@dataclass
class TgBot:
    bot_token: str
    supabase_url: str
    supabase_key: str
    supabase_users_table: str
    supabase_mailing_table: str
    admins_list: list[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(bot_token=env('BOT_TOKEN'),
                               supabase_url=env('SUPABASE_URL'),
                               supabase_key=env('SUPABASE_KEY'),
                               supabase_users_table=env('SUPABASE_USERS_TABLE'),
                               supabase_mailing_table=env('SUPABASE_MAILING_TABLE'),
                               admins_list=list(map(int, env.list("ADMINS"))),
                               )
                  )


config: Config = load_config('secrets/.env_dev') if PROJECT_STATUS.lower() == 'test' else load_config('secrets/.env')
USERS_TABLE = config.tg_bot.supabase_users_table
MAILING_TABLE = config.tg_bot.supabase_mailing_table
