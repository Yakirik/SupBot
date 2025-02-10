from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data import LIMIT_TEXT
from database import DatabaseManager
from keyboards import build_history_keyboard, build_main_menu
from logger import get_logger
from states import GetHistoryStateGroup
from syp_api_manager import SypApiManager

router = Router()
logger = get_logger(__name__)


@router.message(Command('start'))
async def start_command_handler(message: types.Message, db_manager: DatabaseManager):
    chat_id = message.chat.id
    username = message.from_user.username
    if not await db_manager.get_user(chat_id):
        logger.info(f'User {username} joined the chat')
        try:
            await db_manager.add_user(chat_id, username)
        except Exception as e:
            logger.error(e)
    await message.answer(text=f'Hello {username}', reply_markup=build_main_menu())


@router.message(Command('menu'))
async def menu_command_handler(message: types.Message):
    await message.answer(text='her', reply_markup=build_main_menu())


@router.message(F.text == 'Balance')
async def balance_handler(
    message: types.Message, syp_api_manager: SypApiManager, db_manager: DatabaseManager
):
    chat_id = message.chat.id
    card_number = await db_manager.get_card_number(chat_id)
    if not card_number:
        await message.answer(text='First set card')
    elif balance := await syp_api_manager.get_balance(card_number):
        await message.answer(text=f'Current balance: {balance}₽')
    else:
        await message.answer(text='Failed to get balance')


@router.message(F.text == 'Limit')
async def limit_handler(
    message: types.Message, syp_api_manager: SypApiManager, db_manager: DatabaseManager
):
    chat_id = message.chat.id
    card_number = await db_manager.get_card_number(chat_id)
    if not card_number:
        await message.answer(text='First set card')
    elif limit := await syp_api_manager.get_limit(card_number):
        await message.answer(
            text=LIMIT_TEXT.format(limit=limit[0], used=limit[1], balance=(limit[0] - limit[1]))
        )
    else:
        await message.answer(text='Failed to get limit')


@router.message(F.text == 'Get card number')
async def get_card_number_handler(
    message: types.Message, syp_api_manager: SypApiManager, db_manager: DatabaseManager
):
    chat_id = message.chat.id
    card_number = await db_manager.get_card_number(chat_id)
    if not card_number:
        await message.answer(text='First set card')
    else:
        await message.answer(text=f'{card_number}', reply_markup=build_main_menu())


@router.message(F.text == 'History')
async def history_handler(message: types.Message, state: FSMContext):
    await message.answer(text='Select period', reply_markup=build_history_keyboard())
    await state.set_state(GetHistoryStateGroup.choose_period)
