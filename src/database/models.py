from sqlalchemy import BigInteger, String, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    card_number: Mapped[int] = mapped_column(BigInteger, nullable=True)
    balance: Mapped[int] = mapped_column(Numeric, nullable=True)
    last_get_balance_request: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    last_get_history_request: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    last_get_limit_request: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    last_transaction: Mapped[str] = mapped_column(String, nullable=True)
