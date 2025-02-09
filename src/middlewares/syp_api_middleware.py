from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from syp_api_manager import SypApiManager

class SypApiMiddleware(BaseMiddleware):
    syp_api_manager: SypApiManager
    
    def __init__(self, syp_api_manager: SypApiManager) -> None:
        self.syp_api_manager = syp_api_manager

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject, 
        data: Dict[str, Any]) -> Any:
            data['syp_api_manager'] = self.syp_api_manager
            return await handler(event, data)