from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext 
from keyboards.keyboard_builder import build_main_menu, build_history_keyboard
from states import SetCardStateGroup, GetHistoryStateGroup
from data import history_callback_data
from aiogram.types import CallbackQuery
import re
router = Router()

@router.message(Command('start', 'menu'))
async def start_menu_command_handler(message: types.Message):
    await message.answer(reply_markup=build_main_menu())

@router.message(F.text == 'Balance')
async def balance_handler(message: types.Message):
    await message.answer(text='idi naguy')

@router.message(F.text == 'Limit')
async def limit_handler(message: types.Message):
    await message.answer(text='idi naguy')

@router.message(F.text == 'Get card number')
async def get_card_number_handler(message: types.Message):
    await message.answer(text='idi naguy')

@router.message(F.text == 'Set card number')
async def set_card_number_handler(message: types.Message, state: FSMContext):
    await state.set_state(SetCardStateGroup.wait_card)
    await message.answer(text='Type your card')

@router.message(SetCardStateGroup.wait_card)
async def process_card_number_handler(message: types.Message, state: FSMContext):
    await state.clear()
    if not re.match(r'^\d{13}$', message.text):
        await message.answer(text='Card number must be a 13-symbols numeric')
    else:
        await message.answer(text='all good', reply_markup=build_main_menu())

@router.message(F.text == 'History')
async def history_handler(message: types.Message, state: FSMContext):
    await message.answer(text='Select period', reply_markup=build_history_keyboard())
    await state.set_state(GetHistoryStateGroup.choose_period)

@router.callback_query(F.data.in_(history_callback_data.values()), GetHistoryStateGroup.choose_period)
async def history_period_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(period = callback_query.data)
    await callback_query.message.answer(text=callback_query.data, reply_markup=build_main_menu())
    await state.clear()
