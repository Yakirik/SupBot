import asyncio
import logging
import os
from logging import FileHandler, Formatter, Logger

from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv

from database import DatabaseManager
from handlers import main_router
from middlewares import DatabaseMiddleware, SypApiMiddleware
from syp_api_manager import SypApiManager

load_dotenv(find_dotenv())
BOT_TOKEN = os.getenv('BOT_TOKEN')


class SypBot:
    db_manager: DatabaseManager
    syp_api_manager: SypApiManager
    logger: Logger

    def __init__(self, token):
        self.bot = Bot(token)
        self.dispatcher = Dispatcher()
        self.logger = self.get_logger()
        self.dispatcher.startup.register(self.on_startup)
        self.dispatcher.shutdown.register(self.on_shutdown)
        self.dispatcher.include_router(main_router)

    async def run(self):
        await self.dispatcher.start_polling(self.bot)

    async def on_startup(self):
        self.db_manager = DatabaseManager()
        self.syp_api_manager = SypApiManager()
        await self.db_manager.create_db()
        self.dispatcher.update.middleware(DatabaseMiddleware(db_manager=self.db_manager))
        self.dispatcher.update.middleware(SypApiMiddleware(syp_api_manager=self.syp_api_manager))
        asyncio.create_task(self.notificate())

    async def on_shutdown(self):
        await self.syp_api_manager.session.close()

    async def notificate(self):
        while True:
            # users = await self.db_manager.get_users()
            # for user in users:
            # last_db_transaction = await self.db_manager.get_last_transaction(user.chat_id)
            # history = await self.syp_api_manager.get_history(user.chat_id, 1)
            # if history[0]['date'] == last_db_transaction.date:
            #     continue
            # await self.bot.send_message(user.chat_id, 'lol')
            # await self.db_manager.edit_transaction(last_db_transaction.id)
            # await self.db_manager.add_transaction()
            await asyncio.sleep(10)

    def get_logger(self):
        logger = logging.getLogger('main')
        logging.basicConfig(level=logging.INFO)
        handler = FileHandler('syp_bot.log')
        handler.setFormatter(
            Formatter(
                '[%(asctime)s][%(levelname)s] %(message)s',
                '%Y-%m-%d %H:%M:%S',
            )
        )
        logger.addHandler(handler)


if __name__ == "__main__":
    bot = SypBot(BOT_TOKEN)
    asyncio.run(bot.run())
