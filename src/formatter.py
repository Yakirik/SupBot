from datetime import datetime

from data import HISTORY_TEXT
from database import Transaction


class Formatter:
    @classmethod
    def format_transaction(cls, transaction: dict) -> str:
        return HISTORY_TEXT.format(
            name=transaction['locationName'],
            mcc=transaction['mcc'],
            amount=transaction['amount'],
            date=cls.convert_datetime_to_str(transaction['date']),
        )

    @classmethod
    def format_new_transaction(cls, transaction: Transaction, balance: int) -> str:
        formatted_transaction = cls.format_transaction(transaction)
        return (
            'New transaction\n'
            f'{formatted_transaction}\n'
            f'Balance: {(balance - transaction.amount)}₽'
        )

    @classmethod
    def convert_iso_to_datetime(cls, date_str: str) -> datetime:
        return datetime.fromisoformat(date_str)

    @classmethod
    def convert_datetime_to_str(cls, date_str: str) -> str:
        return date_str.strftime('%H:%M %d %B %Y')


# if __name__ == '__main__':
#     print(Formatter.format_transaction())
