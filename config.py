from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    bot_token: str
    supabase_url: str
    supabase_key: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(bot_token=env('BOT_TOKEN'),
                               supabase_url=env('SUPABASE_URL'),
                               supabase_key=env('SUPABASE_KEY')))
