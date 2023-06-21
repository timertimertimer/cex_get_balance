import os
from binance.spot import Spot as Client

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')


class MyBinance:
    def __init__(self):
        self.client = Client(api_key, api_secret)
        self.finalized_assets = dict()

    def get_balance(self) -> float:
        balance = 0

        # main + funding
        assets = self.client.user_asset() + self.client.funding_wallet()
        for asset in assets:
            ticker = asset['asset']
            amount = float(asset['free']) + float(asset['locked'])
            btcValuation = float(asset['btcValuation'])
            if ticker not in self.finalized_assets:
                self.finalized_assets[ticker] = {
                    'amount': amount, 'btcValuation': btcValuation}
            else:
                self.finalized_assets[ticker]['amount'] += amount
                self.finalized_assets[ticker]['btcValuation'] += btcValuation
        btc_avg_price = float(self.client.avg_price('BTCUSDT')['price'])
        for ticker, amount in self.finalized_assets.items():
            total = amount['btcValuation'] * btc_avg_price
            self.finalized_assets[ticker]['total'] = total
            balance += total
        print(f"Total balance: {balance}$")
        self.finalized_assets['total'] = balance
        return self.finalized_assets


if __name__ == "__main__":
    binance = MyBinance()
    print(f'Total balance: {binance.get_balance()}')
