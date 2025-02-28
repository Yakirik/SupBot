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
                    timezone = user.timezone
                    chat_id = user.chat_id
                    card_number = user.card_number
                    history = await self.syp_api_manager.get_history(card_number)

                    if not history:
                        print('history issue')
                        continue

                    last_db_transaction = await self.db_manager.get_last_transaction(
                        session, chat_id
                    )
                    last_api_transaction_time = Formatter.to_timezone(
                        history[0]['date'],
                        'Europe/Moscow',
                    )

                    if not last_db_transaction:
                        print('last_db_trans is empty')
                        for transaction in reversed(history):
                            transaction['date'] = Formatter.to_timezone(
                                transaction['date'],
                                'Europe/Moscow',
                            )
                            await self.db_manager.edit_last_transaction(session, chat_id)
                            await self.db_manager.add_transaction(
                                session,
                                transaction,
                                chat_id,
                            )
                        # history[0]['date'] = last_api_transaction_time
                        # await self.db_manager.add_transaction(
                        #     session,
                        #     history[0],
                        #     chat_id,
                        # )
                        continue

                    if last_api_transaction_time == last_db_transaction.date:
                        print('last trans are the same')
                        continue

                    new_transactions = []
                    for transaction in history:
                        transaction['date'] = Formatter.to_timezone(
                            transaction['date'],
                            'Europe/Moscow',
                        )
                        db_transaction_time = last_db_transaction.date
                        print(db_transaction_time)

                        if transaction['date'] <= db_transaction_time:
                            break

                        new_transactions.append(transaction)
                        message += Formatter.format_transaction(transaction)

                    value, used_value = await self.syp_api_manager.get_limit(user.card_number)
                    balance = value - used_value
                    message += f'{balance}'
                    await self.bot.send_message(chat_id, message)
                    for transaction in reversed(new_transactions):
                        await self.db_manager.edit_last_transaction(
                            session,
                            chat_id,
                        )

                        await self.db_manager.add_transaction(session, transaction, chat_id)

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
