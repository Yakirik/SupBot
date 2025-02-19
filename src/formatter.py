from datetime import datetime

from database import Transaction


class Formatter:
    @classmethod
    def format_transaction(cls, transaction: Transaction) -> str:
        return f'{transaction.name}\n' f'-{transaction.amount} ₽\n' f'{transaction.date}\n'

    @classmethod
    def format_new_transaction(cls, transaction: Transaction, balance: int) -> str:
        formatted_transaction = cls.format_transaction(transaction)
        return (
            'New transaction\n'
            f'{formatted_transaction}\n'
            f'Balance: {(balance - transaction.amount)}₽'
        )

    @classmethod
    def convert_str_to_datetime(cls, date_str: str) -> datetime:
        return datetime.fromisoformat(date_str)

    @classmethod
    def convert_datetime_to_str(cls, date_str: datetime) -> str:
        return date_str.strftime('%H:%M %d %B %Y')


# if __name__ == '__main__':
#     print(Formatter.format_transaction())
