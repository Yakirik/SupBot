import asyncio
import logging
import os
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv, find_dotenv
from database import DatabaseManager
from handlers import main_router
from syp_api_manager import SypApiManager
from middlewares import DatabaseMiddleware, SypApiMiddleware
from logging import DEBUG, FileHandler, Formatter, Logger

class SypBot():
    db_manager: DatabaseManager
    syp_api_manager: SypApiManager

    def __init__(self, token):
        self.bot = Bot(token)
        self.dispatcher = Dispatcher()
        
        self.dispatcher.startup.register(self.on_startup)
        self.dispatcher.shutdown.register(self.on_shutdown)
        self.dispatcher.include_router(main_router)

    async def run(self):
        await self.dispatcher.start_polling(self.bot)

    async def on_startup(self):
        logging.basicConfig(level=logging.INFO)
        self.db_manager = DatabaseManager()
        self.syp_api_manager = SypApiManager()
        await self.db_manager.create_db()
        self.dispatcher.update.middleware(DatabaseMiddleware(db_manager=self.db_manager))
        self.dispatcher.update.middleware(SypApiMiddleware(syp_api_manager=self.syp_api_manager))

    async def on_shutdown(self):
        await self.syp_api_manager.session.close()

    def set_logging(self):
        logger = Logger('syp_bot_logger', DEBUG)
        handler =FileHandler('syp_bot.log')
        handler.setFormatter(
            Formatter(
                '[%(asctime)s][%(levelname)s] %(message)s',
                '%Y-%m-%d %H:%M:%S',
            )
        )
        logger.addHandler(handler)




if __name__ == "__main__":
    load_dotenv(find_dotenv())
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    botik = SypBot(BOT_TOKEN)

    asyncio.run(botik.run())