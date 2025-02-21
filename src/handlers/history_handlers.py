from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data import HISTORY_TEXT, history_callback_data
from database import DatabaseManager
from keyboards import build_main_menu
from logger import get_logger
from states import GetHistoryStateGroup
from syp_api_manager import SypApiManager

router = Router()
logger = get_logger(__name__)


@router.callback_query(
    F.data.in_(history_callback_data.values()), GetHistoryStateGroup.choose_period
)
async def select_history_period_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    syp_api_manager: SypApiManager,
    db_manager: DatabaseManager,
) -> None:
    chat_id = callback_query.message.chat.id
    async with db_manager.session_pool() as session:
        card_number = await db_manager.get_card_number(session, chat_id)

    if not card_number:
        callback_query.message.answer(text='Set card first')
    elif history := await syp_api_manager.get_history(card_number, int(callback_query.data)):
        answer = 'History\n'
        for transaction in history:
            # time = datetime.fromisoformat(transaction['date']).strftime('%H:%M %d %B %Y')
            time = datetime.strptime(transaction['date'], "%Y-%m-%dT%H:%M:%S.%f%z")
            # time = datetime.strptime(transaction['date'], '%H:%M %d %B %Y')
            answer += HISTORY_TEXT.format(
                name=transaction['locationName'],
                mcc=transaction['mcc'],
                amount=transaction['amount'],
                date=time,
            )
        await callback_query.message.delete()
        await callback_query.message.answer(text=answer, reply_markup=build_main_menu())
    else:
        await callback_query.message.delete()
        await callback_query.message.answer(text='No history', reply_markup=build_main_menu())
    await state.clear()


@router.callback_query(GetHistoryStateGroup.choose_period)
async def back_history_period_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete()
    await callback_query.message.answer(text='Back', reply_markup=build_main_menu())
