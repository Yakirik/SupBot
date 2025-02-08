from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from keyboards.keyboard_builder import KeyboardBuilder



router = Router()


@router.message(Command('start', 'menu'))
async def start_menu_command_handler(message: types.Message):
    await message.answer(text='Меню', reply_markup=KeyboardBuilder.build_main_menu())