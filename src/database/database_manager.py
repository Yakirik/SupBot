import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from formatter import Formatter

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import select
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

    async def add_user(
        self,
        session: AsyncSession,
        chat_id: int,
        username: str,
    ) -> None:
        user = User(
            chat_id=chat_id,
            username=username,
        )
        try:
            session.add(user)
            await session.commit()
        except Exception:
            await session.rollback()

    async def get_user(self, session: AsyncSession, chat_id: int) -> User | None:
        try:
            return await session.get(User, chat_id)
        except Exception:
            await session.rollback()

    async def set_card_number(
        self,
        session: AsyncSession,
        chat_id: int,
        card_number: int,
    ) -> None:
        user = await session.get(User, chat_id)
        if user:
            user.card_number = card_number
            try:
                await session.commit()
            except Exception:
                session.rollback()

    async def get_card_number(self, session: AsyncSession, chat_id: int) -> None:
        user = await session.get(User, chat_id)
        if user:
            try:
                return user.card_number
            except Exception:
                session.rollback()

    async def get_users(self, session: AsyncSession) -> list[User]:
        query = select(User)
        response = await session.execute(query)
        users = response.scalars().all()
        return users

    async def add_transaction(
        self,
        session: AsyncSession,
        transaction: dict,
        chat_id: int,
    ) -> None:
        transaction_date = Formatter.convert_str_to_datetime(transaction['date'])
        user = Transaction(
            merchant_id=transaction['merchantId'],
            location_name=transaction['locationName'],
            mcc=transaction['mcc'],
            amount=transaction['amount'],
            date=transaction_date,
            is_last=True,
            chat_id=chat_id,
        )
        try:
            session.add(user)
            await session.commit()
        except Exception:
            await session.rollback()

    async def get_last_transaction(self, session: AsyncSession, chat_id: int) -> Transaction:
        try:
            query = select(Transaction).filter_by(chat_id=chat_id, is_last=True)
            last_transaction = await session.execute(query)
            return last_transaction
        except Exception:
            pass

    async def edit_last_transaction(self, session: AsyncSession, chat_id: int) -> None:
        try:
            last_transaction = await self.get_last_transaction(session, chat_id)
            last_transaction.is_last = False
            await session.commit()
        except Exception:
            await session.rollback()
