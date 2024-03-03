import aiofiles

from pyrogram.handlers import MessageHandler
from pyrogram import Client, filters
from pyrogram.types import Message


class UserBot:

    def __init__(self, name: str, target: int, card_begin: list, api_id: int, api_hash: str):
        self.target = target
        self.cards = card_begin
        # Welcome message template
        print(f'TARGET:: {self.target}')

        self.client = Client(name=f'session_number:{name}', api_id=api_id, api_hash=api_hash)

    # Target chat. Can also be a list of multiple chat ids/usernames

    def chat_post(self, data):

        async def filter_data(self, client, message: Message):
            return str(self.data) in str(message.chat.id)

        return filters.create(filter_data, data=data)

    async def update_codes(self):
        async with aiofiles.open("codes.txt", "r") as file:
            content = await file.read()
            self.cards = content.split(", ")
            await file.close()

    async def message_chat_id(self, client: Client, message: Message):
        if message.from_user.is_bot:
            if message.reply_markup != None:
                for code in self.cards:
                    if f"💳 Карта: {code}" in message.text:
                        await client.request_callback_answer(
                            chat_id=message.chat.id,
                            message_id=message.id,
                            callback_data=message.reply_markup.inline_keyboard[0][0].callback_data)

    async def starts(self):
        self.client.add_handler(MessageHandler(self.message_chat_id, self.chat_post(f'{self.target}')))

        return self.client
