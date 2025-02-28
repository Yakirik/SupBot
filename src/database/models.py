from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'user'

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    card_number: Mapped[int | None]
    balance: Mapped[int | None] = mapped_column(Numeric, nullable=True)
    timezone: Mapped[str | None] = mapped_column(String, default='Europe/Moscow')
    last_get_balance_request: Mapped[datetime | None]
    last_get_history_request: Mapped[datetime | None]
    last_get_limit_request: Mapped[datetime | None]
    last_transaction: Mapped[str | None]


class Transaction(Base):
    __tablename__ = 'transaction'

    id: Mapped[int] = mapped_column(primary_key=True)
    merchant_id: Mapped[int | None]
    location_name: Mapped[str | None]
    mcc: Mapped[int | None]
    amount: Mapped[int | None]
    date: Mapped[datetime | None]
    is_last: Mapped[bool | None]
    chat_id: Mapped[int] = Column(Integer, ForeignKey('user.chat_id'))  # foreign key
