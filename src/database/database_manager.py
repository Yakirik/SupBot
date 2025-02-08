import os
from sqlalchemy.ext.asyncio import  async_sessionmaker, create_async_engine, AsyncSession

from .models import User, Base
from dotenv import load_dotenv

class DatabaseManager:

    def __init__(self):
        load_dotenv()
        self.engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))
        self.async_session_generator = async_sessionmaker(self.engine, class_=AsyncSession)

    @staticmethod
    async def create_db() -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_user(session: AsyncSession, data: dict) -> None:
        obj = User(
            chat_id=data['chat_id'],
            username=data['username'],
        )
        session.add(obj)
        await session.commit()

    @staticmethod
    async def set_card_number(session: AsyncSession, data: dict) -> None:
        obj = await session.get(User, data['chat_id'])
        if obj:
            obj.card_number = data['card_number']
            await session.commit()

    @staticmethod
    async def get_card_number(session: AsyncSession, data: dict) -> None:
        obj = await session.get(User, data['chat_id'])
        if obj:
            return obj.card_number