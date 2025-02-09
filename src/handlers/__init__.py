from .history_handlers import router as history_router
from .card_number_handlers import router as card_number_router
from .default_handlers import router as default_router
from aiogram import Router

main_router = Router()
main_router.include_routers(
    history_router,
    card_number_router,
    default_router,
)

__all__= [
    'main_router',
]