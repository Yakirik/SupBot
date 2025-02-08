import asyncio
import logging
import os
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv, find_dotenv
from database import DatabaseManager
from handlers import main_router


class BotCore:
    async def get_balance(self):
        pass

    async def get_limit(self):
        pass

    async def get_history(self):
        pass

    async def get_card_number(self):
        pass

    async def set_card_number(self):
        pass


class SypBot():
    def __init__(self, token):
        self.bot = Bot(token)
        self.dispatcher = Dispatcher()
        
        self.dispatcher.startup.register(self.on_startup)

        self.dispatcher.include_router(main_router)

    async def run(self):
        await self.dispatcher.start_polling(self.bot)

    async def on_startup(self):
        logging.basicConfig(level=logging.INFO)
        # await DatabaseManager.create_db()



if __name__ == "__main__":
    load_dotenv(find_dotenv())
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    botik = SypBot(BOT_TOKEN)

    asyncio.run(botik.run())