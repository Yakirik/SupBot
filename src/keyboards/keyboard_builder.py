from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from data import callback_back, history_callback_data, timezone_callback_data


def build_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='Balance')
    builder.button(text='Limit')
    builder.button(text='History')
    builder.button(text='Set timezone')
    builder.button(text='Get card number')
    builder.button(text='Set card number')

    builder.adjust(4)

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


def build_timezone_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Novosibirsk', callback_data=timezone_callback_data['Novosibirsk'])
    builder.button(text='Moscow', callback_data=timezone_callback_data['Moscow'])
    builder.button(text='Kamchatka (msk +9)', callback_data=timezone_callback_data['Kamchatka'])
    builder.button(text='Sakhalin (msk +8)', callback_data=timezone_callback_data['Sakhalin'])
    builder.button(text='Omsk (msk +3)', callback_data=timezone_callback_data['Omsk'])
    builder.button(
        text='Yekaterinburg (msk +2)', callback_data=timezone_callback_data['Yekaterinburg']
    )
    builder.button(text='Samara (msk +1)', callback_data=timezone_callback_data['Samara'])
    builder.button(
        text='Kaliningrad (msk -1)', callback_data=timezone_callback_data['Kaliningrad']
    )
    builder.button(text='Back', callback_data=callback_back)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
