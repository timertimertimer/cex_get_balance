import os
from config import usd_tickers
from kucoin.client import User, Market

api_key = os.getenv('KUCOIN_API_KEY')
api_secret = os.getenv('KUCOIN_API_SECRET')
api_passphrase = os.getenv('KUCOIN_API_PASSPHRASE')


class MyKucoin:
    def __init__(self):
        self.client = User(api_key, api_secret, api_passphrase)
        self.market = Market(api_key, api_secret, api_passphrase)
        self.finalized_assets = dict()

    def get_balance(self) -> float:
        # main + trade
        print('Kucoin balance')
        assets = self.client.get_account_list()
        for asset in assets:
            if asset['currency'] not in self.finalized_assets:
                self.finalized_assets[asset['currency']
                                      ] = float(asset['balance'])
            else:
                self.finalized_assets[asset['currency']
                                      ] += float(asset['balance'])

        balance = 0
        for ticker, amount in self.finalized_assets.items():
            if ticker in usd_tickers:
                price = 1
            else:
                price = float(self.market.get_ticker(
                    f"{ticker}-USDT")['price'])
            total = price * amount
            balance += total
            print(f"{amount} {ticker} = {total}$")
        print(f"Total balance: {balance}$")
        return balance


if __name__ == "__main__":
    kucoin = MyKucoin()
    print(f'Total balance: {kucoin.get_balance()}')
