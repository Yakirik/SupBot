history_callback_data = {
    '1 day': '1',
    '3 days': '3',
    '7 days': '7',
    '1 month': '30',
}
callback_back = 'Back'

LIMIT_TEXT = """
Today's limit: {limit} ₽
Used: {used} ₽
Balance: {balance} ₽
"""

HISTORY_TEXT = """
{name} (mcc {mcc})
{amount} ₽
{date}
"""

HELP_TEXT = """
Commands:
/start
/help
/balance
/getcardnumber
/setcardnumber
"""
