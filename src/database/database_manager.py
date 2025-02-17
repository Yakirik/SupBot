import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import Base, Transaction, User


class DatabaseManager:
    engine: AsyncEngine
    session_pool: AsyncSession

    def __init__(self):
        load_dotenv(find_dotenv())
        self.engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))
        self.session_pool = async_sessionmaker(self.engine, class_=AsyncSession)

    async def create_db(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_user(self, chat_id: int, username: str) -> None:
        obj = User(
            chat_id=chat_id,
            username=username,
        )
        async with self.session_pool() as session:
            session.add(obj)
            await session.commit()

    async def get_user(self, chat_id: int) -> User | None:
        async with self.session_pool() as session:
            try:
                return await session.get(User, chat_id)
            except Exception:
                pass

    async def set_card_number(self, chat_id: int, card_number: int) -> None:
        async with self.session_pool() as session:
            obj = await session.get(User, chat_id)
            if obj:
                obj.card_number = card_number
                await session.commit()

    async def get_card_number(self, chat_id: int) -> None:
        async with self.session_pool() as session:
            obj = await session.get(User, chat_id)
            if obj:
                return obj.card_number

    async def get_users(self) -> None:
        pass

    async def get_last_transaction(self, chat_id: int) -> Transaction:
        pass

    async def edit_transaction(self, transaction_id: int) -> None:
        pass

    async def add_transaction(self, transaction: Transaction) -> None:
        pass
