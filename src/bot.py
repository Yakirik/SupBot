import asyncio
import logging
import os
from datetime import datetime
from formatter import Formatter
from logging import FileHandler
from logging import Formatter as logging_formatter
from logging import Logger

import pytz
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
            async with self.db_manager.session_pool() as session:
                users = await self.db_manager.get_users(session)
                for user in users:
                    message = 'New trasaction(s):\n'
                    last_db_transaction = await self.db_manager.get_last_transaction(
                        session, user.chat_id
                    )
                    history = await self.syp_api_manager.get_history(user.card_number)

                    if not history:
                        print('history issue')
                        continue
                    if not last_db_transaction:
                        print('last_db_trans is empty')
                        history[0]['date'] = datetime.fromisoformat(history[0]['date'])
                        await self.db_manager.add_transaction(session, history[0], user.chat_id)
                        continue
                    if datetime.fromisoformat(history[0]['date']) == last_db_transaction.date:
                        print('last trans are the same')
                        continue

                    new_transactions = []
                    for transaction in history:
                        transaction['date'] = datetime.fromisoformat(transaction['date'])
                        db_transaction_time = last_db_transaction.date
                        db_transaction_time = db_transaction_time.astimezone(
                            pytz.timezone('Europe/Moscow')
                        )
                        # api_transaction_time = api_transaction_time.astimezone(
                        #     pytz.timezone('Europe/Moscow')
                        # )
                        if transaction['date'] <= db_transaction_time:
                            break
                        new_transactions.append(transaction)
                        message += Formatter.format_transaction(transaction)

                    for transaction in reversed(new_transactions):
                        await self.db_manager.edit_last_transaction(
                            session,
                            user.chat_id,
                        )

                        await self.db_manager.add_transaction(
                            session,
                            transaction,
                            user.chat_id,
                        )

                    value, used_value = await self.syp_api_manager.get_balance(user.card_number)
                    balance = value - used_value
                    message += f'{balance}'
                    await self.bot.send_message(user.chat_id, message)
            await asyncio.sleep(180)

    def get_logger(self):
        logger = logging.getLogger('main')
        logging.basicConfig(level=logging.INFO)
        handler = FileHandler('syp_bot.log')
        handler.setFormatter(
            logging_formatter(
                '[%(asctime)s][%(levelname)s] %(message)s',
                '%Y-%m-%d %H:%M:%S',
            )
        )
        logger.addHandler(handler)


if __name__ == "__main__":
    bot = SypBot(BOT_TOKEN)
    asyncio.run(bot.run())
