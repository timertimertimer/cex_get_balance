from config import *
from kucoin.client import User, Market

api_key = os.getenv('KUCOIN_API_KEY') or envs['KUCOIN_API_KEY']
api_secret = os.getenv('KUCOIN_API_SECRET') or envs['KUCOIN_API_SECRET']
api_passphrase = os.getenv('KUCOIN_API_PASSPHRASE') or envs['KUCOIN_API_PASSPHRASE']


class MyKucoin:
    def __init__(self):
        self.client = User(api_key, api_secret, api_passphrase)
        self.market = Market(api_key, api_secret, api_passphrase)
        self.finalized_assets = dict()

    def get_balance(self) -> float:
        # main + trade
        assets = self.client.get_account_list()
        for asset in assets:
            ticker = asset['currency']
            if ticker not in self.finalized_assets:
                self.finalized_assets[ticker] = {'amount': float(asset['balance'])}
            else:
                self.finalized_assets[ticker]['amount'] += float(asset['balance'])

        balance = 0
        for ticker, amount in self.finalized_assets.items():
            if ticker in usd_tickers:
                price = 1
            else:
                price = float(self.market.get_ticker(
                    f"{ticker}-USDT")['price'])
            total = price * amount['amount']
            self.finalized_assets[ticker]['total'] = total
            balance += total
        print(f"Total balance: {balance}$")
        self.finalized_assets['total'] = balance
        return self.finalized_assets


if __name__ == "__main__":
    kucoin = MyKucoin()
    print(f'Total balance: {kucoin.get_balance()}')
