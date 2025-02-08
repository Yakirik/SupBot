from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

class KeyboardBuilder:

    @staticmethod
    def build_main_menu() -> ReplyKeyboardMarkup:
        buttons = [
            'Balance',
            'Limit',
            'History',
            'Get card number',
            'Set card number'
        ]
        builder = ReplyKeyboardBuilder()

        for button in buttons:
            builder.button(text=button)
        builder.adjust(3)

        return builder.as_markup(resize_keyboard=True)