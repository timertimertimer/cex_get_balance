import os
from binance.spot import Spot as Client

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')


class MyBinance:
    def __init__(self):
        self.client = Client(api_key, api_secret)

    def get_balance(self) -> float:
        print('Binance balance')
        balance = 0

        # main + funding
        assets = self.client.user_asset() + self.client.funding_wallet()
        finalized_assets = dict()
        for asset in assets:
            ticker = asset['asset']
            amount = float(asset['free']) + float(asset['locked'])
            btcValuation = float(asset['btcValuation'])
            if ticker not in finalized_assets:
                finalized_assets[ticker] = {
                    'amount': amount, 'btcValuation': btcValuation}
            else:
                finalized_assets[ticker]['amount'] += amount
                finalized_assets[ticker]['btcValuation'] += btcValuation
        btc_avg_price = float(self.client.avg_price('BTCUSDT')['price'])
        for ticker, amount in finalized_assets.items():
            total = amount['btcValuation'] * btc_avg_price
            balance += total
            print(f'{amount["amount"]} {ticker} = {total}$')
        print(f"Total balance: {balance}$")
        return balance


if __name__ == "__main__":
    binance = MyBinance()
    print(f'Total balance: {binance.get_balance()}')
