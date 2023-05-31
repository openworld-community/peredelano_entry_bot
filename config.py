from dataclasses import dataclass

from environs import Env

PROJECT_STATUS = 'prod'


@dataclass
class TgBot:
    bot_token: str
    supabase_url: str
    supabase_key: str
    supabase_table: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(bot_token=env('BOT_TOKEN'),
                               supabase_url=env('SUPABASE_URL'),
                               supabase_key=env('SUPABASE_KEY'),
                               supabase_table=env('SUPABASE_TABLE'))
                  )


config: Config = load_config('.env_dev') if PROJECT_STATUS.lower() == 'test' else load_config()
DB_TABLE = config.tg_bot.supabase_table
