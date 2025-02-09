import aiohttp
from pprint import pprint
from datetime import datetime, timedelta

class SypApiManager:
    session: aiohttp.ClientSession

    def __init__(self):
        self.session = aiohttp.ClientSession()
    
    async def get_balance(self, card_number: int):
        url = f'https://meal.gift-cards.ru/api/1/cards/{card_number}'
        async with self.session.get(url) as response:
            resp = await response.json()
            try:
                return str(resp['data']['balance']['availableAmount'])
            except Exception as e:
                pprint(resp)
                return 'Failed to get balance'
                
    async def get_limit(self, card_number):
        url = f'https://meal.gift-cards.ru/api/1/cards/{card_number}/limits'

        async with self.session.get(url) as response:
            limit = await response.json()
            try:
                print(limit)
                limit = limit['data']['limits'][0]
                return limit['value'], limit['usedValue']
            except Exception as e:
                return None
            
    async def get_history(self, card_number, days: int):
        url = f'https://meal.gift-cards.ru/api/1/cards/{card_number}'

        async with self.session.get(url) as response:
            history = await response.json()
            try:
                history = history['data']['history']
                return [
                    {
                        'name': transaction['locationName'][0],
                        'mcc': transaction['mcc'],
                        'amount': transaction['amount'],
                        'date': transaction['time'],
                    }
                    for transaction in history
                    if transaction['time'] >= (datetime.now() - timedelta(days=days)).isoformat()
                ]
            except Exception as e:
                print(e)
                return None