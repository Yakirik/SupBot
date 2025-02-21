import os

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
                pass

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
        try:
            user = Transaction(
                merchant_id=transaction['merchantId'],
                location_name=transaction['locationName'],
                mcc=transaction['mcc'],
                amount=transaction['amount'],
                date=transaction['date'],
                is_last=True,
                chat_id=chat_id,
            )
        except Exception:
            print('failed to create new transaction')
        try:
            session.add(user)
            await session.commit()
        except Exception:
            print('failed to commit new transaction')
            # await session.rollback()

    async def get_last_transaction(self, session: AsyncSession, chat_id: int) -> Transaction:
        try:
            query = select(Transaction).filter_by(chat_id=chat_id, is_last=True)
            res = await session.execute(query)
            last_transaction = res.scalars().first()
            # print(last_transaction)
            if last_transaction:
                return last_transaction
            else:
                return None
        except Exception:
            print('lol')
            return None

    async def edit_last_transaction(self, session: AsyncSession, chat_id: int) -> None:
        try:
            last_transaction = await self.get_last_transaction(session, chat_id)
            last_transaction.is_last = False
            await session.commit()
        except AttributeError:
            pass
        except Exception:
            await session.rollback()
