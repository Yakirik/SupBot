import re

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from database import DatabaseManager
from keyboards import build_main_menu
from logger import get_logger
from states import SetCardStateGroup

router = Router()
logger = get_logger(__name__)


@router.message(F.text == 'Set card number')
async def set_card_number_handler(message: types.Message, state: FSMContext):
    await state.set_state(SetCardStateGroup.wait_card)
    await message.answer(text='Type your card')


@router.message(SetCardStateGroup.wait_card)
async def process_card_number_handler(
    message: types.Message, state: FSMContext, db_manager: DatabaseManager
):
    await state.clear()
    if not re.match(r'^\d{13}$', message.text):
        await message.answer(text='Card number must be a 13-symbols numeric')
    else:
        chat_id = message.chat.id
        async with db_manager.session_pool() as session:
            await db_manager.set_card_number(session, chat_id, int(message.text))
        await message.answer(
            text=f'Card number set to {message.text}', reply_markup=build_main_menu()
        )
