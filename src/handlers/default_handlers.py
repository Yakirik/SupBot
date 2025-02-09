from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext 
from keyboards import build_main_menu, build_history_keyboard
from states import GetHistoryStateGroup
from data import LIMIT_TEXT
from database import DatabaseManager
from syp_api_manager import SypApiManager

router = Router()

@router.message(Command('start'))
async def start_command_handler(message: types.Message, db_manager: DatabaseManager):
    chat_id = message.chat.id
    username = message.chat.username
    if not await db_manager.get_user(chat_id):
        await db_manager.add_user(chat_id, username)
    await message.answer(text='her', reply_markup=build_main_menu())

@router.message(Command('menu'))
async def menu_command_handler(message: types.Message):
    await message.answer(text='her', reply_markup=build_main_menu())

@router.message(F.text == 'Balance')
async def balance_handler(message: types.Message, syp_api_manager: SypApiManager):
    chat_id = message.chat.id
    balance = await syp_api_manager.get_balance(chat_id)
    await message.answer(text=balance)
    # if not balance:
    #     await message.answer(text='Failed to get balance')
    # else:
    #     await message.answer(text=balance)

@router.message(F.text == 'Limit')
async def limit_handler(message: types.Message, syp_api_manager: SypApiManager, db_manager: DatabaseManager):
    chat_id = message.chat.id
    card_number = await db_manager.get_card_number(chat_id)
    if not card_number:
        await message.answer(text='First set card')
    elif limit := await syp_api_manager.get_limit(card_number):
        await message.answer(text=LIMIT_TEXT.format(
            limit=limit[0],
            used=limit[1],
            balance=(limit[0] - limit[1])
        ))
    else:
        await message.answer(text='Failed to get limit')

@router.message(F.text == 'Get card number')
async def get_card_number_handler(message: types.Message, syp_api_manager: SypApiManager, db_manager: DatabaseManager):
    chat_id = message.chat.id
    card_number = await db_manager.get_card_number(chat_id)
    if not card_number:
        await message.answer(text='First set card')    
    elif balance := syp_api_manager.get_balance(card_number):
        await message.answer(text=f'Current balance: {balance}₽')
    else:
        await message.answer(text='Failed to get balance')

@router.message(F.text == 'History')
async def history_handler(message: types.Message, state: FSMContext):
    await message.answer(text='Select period', reply_markup=build_history_keyboard())
    await state.set_state(GetHistoryStateGroup.choose_period)