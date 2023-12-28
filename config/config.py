from environs import Env
from dataclasses import dataclass


@dataclass
class UserBot:
    api_id: int
    api_hash: str

@dataclass
class Config:
    chat_id: list
    user_bot: UserBot

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(user_bot=UserBot(
        api_id=env('API_ID'),
        api_hash=env('API_HASH')
    ),
    chat_id=env('CHAT_ID'))
