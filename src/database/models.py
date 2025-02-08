from sqlalchemy import BigInteger, String, Numeric, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = 'user'

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    card_number: Mapped[int | None]
    balance: Mapped[int | None] = mapped_column(Numeric, nullable=True)
    last_get_balance_request: Mapped[datetime | None]
    last_get_history_request: Mapped[datetime | None]
    last_get_limit_request: Mapped[datetime | None]
    last_transaction: Mapped[str | None]
