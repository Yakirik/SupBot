from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data import timezone_callback_data
from database import DatabaseManager
from keyboards import build_main_menu, build_timezone_keyboard
from logger import get_logger
from states import SetTimeZoneStateGroup

router = Router()
logger = get_logger(__name__)


@router.message(F.text == 'Set timezone')
async def timezone_handler(message: types.Message, state: FSMContext):
    await message.answer(text='Select timezone', reply_markup=build_timezone_keyboard())
    await state.set_state(SetTimeZoneStateGroup.choose_timezone)


@router.callback_query(
    F.data.in_(timezone_callback_data.values()), SetTimeZoneStateGroup.choose_timezone
)
async def select_timezone_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    db_manager: DatabaseManager,
) -> None:
    chat_id = callback_query.message.chat.id

    try:
        async with db_manager.session_pool() as session:
            await db_manager.edit_timezone(session, chat_id, callback_query.data)
        await callback_query.message.delete()
        await callback_query.message.answer(text='success', reply_markup=build_main_menu())
    except Exception:
        await callback_query.message.delete()
        await callback_query.message.answer(text='fail', reply_markup=build_main_menu())
    await state.clear()


@router.callback_query(SetTimeZoneStateGroup.choose_timezone)
async def back_history_period_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(text='Back', reply_markup=build_main_menu())
    await state.clear()
