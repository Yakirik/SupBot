import asyncio
import logging
import os
from aiogram import Dispatcher, Bot
from handlers import main_router
from dotenv import load_dotenv
from database import get_db_session


class BotCore:
    def get_balance(self):
        pass

    def get_limit(self):
        pass        

    def get_history(self):
        pass

    def get_card_number(self):
        pass

    def set_card_number(self):
        pass


class FoodFinderBot(BotCore):
    def __init__(self, token):
        self.bot = Bot(token)
        async_db_session = get_db_session()

        logging.basicConfig(level=logging.INFO)
        self.dispatcher = Dispatcher()

        self.dispatcher.include_router(main_router)

    async def run(self):
        await self.dispatcher.start_polling(self.bot)



if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    botik = FoodFinderBot(BOT_TOKEN)

    asyncio.run(botik.run())