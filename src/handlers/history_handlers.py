from datetime import datetime
from formatter import Formatter

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data import HISTORY_TEXT, history_callback_data
from database import DatabaseManager
from keyboards import build_history_keyboard, build_main_menu
from logger import get_logger
from states import GetHistoryStateGroup
from syp_api_manager import SypApiManager

router = Router()
logger = get_logger(__name__)


@router.message(F.text == 'History')
async def history_handler(message: types.Message, state: FSMContext, db_manager: DatabaseManager):
    chat_id = message.chat.id
    async with db_manager.session_pool() as session:
        user = await db_manager.get_user(session, chat_id)

        if user.last_get_history_request:
            if (datetime.now() - user.last_get_history_request).seconds < 300:
                await message.answer(text='cooldown')
                return

        user.last_get_history_request = datetime.now()
        await session.commit()

    await message.answer(text='Select period', reply_markup=build_history_keyboard())
    await state.set_state(GetHistoryStateGroup.choose_period)


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
        user = await db_manager.get_user(session, chat_id)

    if not card_number:
        await callback_query.message.answer(text='Set card first')
    elif history := await syp_api_manager.get_history(card_number, int(callback_query.data)):
        answer = 'History\n'
        for transaction in history:
            time = Formatter.to_timezone(transaction['date'], user.timezone)
            time = Formatter.convert_datetime_to_str(time)
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
