from pybit.unified_trading import HTTP
from config import *

api_key = os.getenv('BYBIT_API_KEY') or envs['BYBIT_API_KEY']
api_secret = os.getenv('BYBIT_API_SECRET') or envs['BYBIT_API_SECRET']


class MyByBit:
    def __init__(self):
        self.session = HTTP(
            testnet=False,
            api_key=api_key,
            api_secret=api_secret,
        )
        self.finalized_assets = dict()
        self.spot = self.session.get_coins_balance(accountType="SPOT")
        self.fund = self.session.get_coins_balance(accountType="FUND")

    def get_balance(self) -> dict:
        if self.spot['retMsg'] == 'success' and self.fund['retMsg'] == 'success':
            coins = self.spot['result']['balance'] + \
                    self.fund['result']['balance']
            for coin in coins:
                ticker = coin['coin']
                amount = float(coin['walletBalance'])
                if ticker not in self.finalized_assets:
                    self.finalized_assets[ticker] = {'amount': amount}
                else:
                    self.finalized_assets[ticker]['amount'] += amount
        else:
            print(self.spot['retMsg'])
            print(self.fund['retMsg'])
            return 0

        # Total in $
        balance = 0
        for ticker, amount in self.finalized_assets.items():
            if ticker in usd_tickers:
                price = 1
            else:
                response = self.session.get_tickers(
                    category='spot', symbol=f'{ticker}USDT')
                if response['retMsg'] == 'OK':
                    price = float(response['result']['list'][0]['lastPrice'])
                else:
                    price = None
                    print(response['retMsg'])
            if price is not None:
                total = price * amount['amount']
                self.finalized_assets[ticker]['total'] = total
                balance += total
            else:
                self.finalized_assets[ticker]['total'] = -1
        print(f"Total balance: {balance}$")
        self.finalized_assets['total'] = balance
        return self.finalized_assets


if __name__ == "__main__":
    bybit = MyByBit()
    print(f'Total balance: {bybit.get_balance()}')
