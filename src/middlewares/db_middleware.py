from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from database import DatabaseManager

class DatabaseMiddleware(BaseMiddleware):
    db_manager: DatabaseManager
    
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject, 
        data: Dict[str, Any]) -> Any:
            data['db_manager'] = self.db_manager
            return await handler(event, data)