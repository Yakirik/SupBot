from datetime import datetime

import pytz

from data import HISTORY_TEXT


class Formatter:
    @classmethod
    def format_transaction(cls, transaction: dict, timezone: str) -> str:
        return HISTORY_TEXT.format(
            name=transaction['locationName'],
            mcc=transaction['mcc'],
            amount=transaction['amount'],
            date=cls.convert_datetime_to_str(
                cls.to_timezone(transaction['date'], timezone),
            ),
        )

    @classmethod
    def convert_datetime_to_str(cls, date_str: datetime) -> str:
        return date_str.strftime('%H:%M %d %B %Y')

    @classmethod
    def to_timezone(cls, date_str: str | datetime, timezone: str) -> str:
        if isinstance(date_str, str):
            return (
                datetime.fromisoformat(date_str)
                .astimezone(pytz.timezone(timezone))
                .replace(tzinfo=None)
            )
        elif isinstance(date_str, datetime):
            return date_str.astimezone(pytz.timezone(timezone)).replace(tzinfo=None)
        return date_str


# if __name__ == '__main__':
#     print(Formatter.format_transaction())
