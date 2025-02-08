from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
import os
from dotenv import load_dotenv



def get_db_session():
    load_dotenv()
    engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))
    async_session = async_sessionmaker(engine, class_=AsyncSession)
    return async_session


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())