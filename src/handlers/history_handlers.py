from datetime import datetime
from aiogram import Router, F
from aiogram.fsm.context import FSMContext 
from keyboards import build_main_menu
from states import GetHistoryStateGroup
from data import history_callback_data, HISTORY_TEXT
from aiogram.types import CallbackQuery
from database import DatabaseManager
from syp_api_manager import SypApiManager

router = Router()


@router.callback_query(F.data.in_(history_callback_data.values()), GetHistoryStateGroup.choose_period)
async def select_history_period_handler(callback_query: CallbackQuery, state: FSMContext, syp_api_manager: SypApiManager, db_manager: DatabaseManager):
    chat_id = callback_query.message.chat.id
    card_number = await db_manager.get_card_number(chat_id)
    if not card_number:
        callback_query.message.answer(text='Set card first')
    elif history := await syp_api_manager.get_history(card_number, int(callback_query.data)):
        answer = 'History\n'
        for transaction in history:
            time = datetime.fromisoformat(transaction['date']).strftime('%H:%M %d %B %Y')
            answer += HISTORY_TEXT.format(
                name=transaction['name'],
                mcc=transaction['mcc'],
                amount=transaction['amount'],
                date=time,
            )
        await callback_query.message.answer(text=answer, reply_markup=build_main_menu())
    else:
        await callback_query.message.answer(text='Failed to get history', reply_markup=build_main_menu())
    await state.clear()

@router.callback_query(GetHistoryStateGroup.choose_period)
async def back_history_period_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.delete_reply_markup()
    
