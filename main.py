from pyrogram import Client, filters
from pyrogram.types import Message
from config.config import Config, load_config
from service.service import set_code


config: Config = load_config()

client = Client(name='me_client', api_id=config.user_bot.api_id, api_hash=config.user_bot.api_hash)

# Обработка входящих текстовых сообщений
@client.on_message(filters.incoming & filters.text & filters.me)
def forward_message(client: Client, message: Message):
    set_code(code=message.text)
    

# Запуск клиента Pyrogram
if __name__ == '__main__':
    client.run()