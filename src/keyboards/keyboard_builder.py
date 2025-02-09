from aiogram.types import  ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from data import history_callback_data, callback_back


def build_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='Balance', )
    builder.button(text='Limit',)
    builder.button(text='History',)
    builder.button(text='Get card number',)
    builder.button(text='Set card number',)

    builder.adjust(3)

    return builder.as_markup(resize_keyboard=True)

def build_history_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='1 day', callback_data=history_callback_data['1 day'])
    builder.button(text='3 days', callback_data=history_callback_data['3 days'])
    builder.button(text='7 days', callback_data=history_callback_data['7 days'])
    builder.button(text='1 Month', callback_data=history_callback_data['1 month'])
    builder.button(text='Back', callback_data=callback_back)

    builder.adjust(4)

    return builder.as_markup(resize_keyboard=True)
