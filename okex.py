from okx.Account import AccountAPI
from okx.Funding import FundingAPI
from okx.MarketData import MarketAPI
from config import *

api_key = os.getenv('OKX_API_KEY')
api_secret = os.getenv('OKX_API_SECRET')
passphrase = os.getenv('OKX_API_PASSPHRASE')


class MyOkex:
    def __init__(self):
        self.finalized_assets = dict()
        args = (api_key, api_secret, passphrase, False, '0', 'https://www.okx.com', False)
        self.trading = AccountAPI(*args)
        self.funding = FundingAPI(*args)
        self.market = MarketAPI(*args)

    def get_balance(self):
        assets = self.trading.get_account_balance()['data'][0]['details'] + self.funding.get_balances()['data']
        for asset in assets:
            ticker = asset['ccy']
            amount = asset['cashBal'] if 'cashBal' in asset else asset['bal']
            if ticker not in self.finalized_assets:
                self.finalized_assets[ticker] = {'amount': float(amount)}
            else:
                self.finalized_assets[ticker]['amount'] += float(amount)
        balance = 0
        for ticker, amount in self.finalized_assets.items():
            if ticker in usd_tickers:
                price = 1
            else:
                price = float(self.market.get_ticker(
                    f"{ticker}-USDT")['data'][0]['askPx'])
            total = price * amount['amount']
            self.finalized_assets[ticker]['total'] = total
            balance += total
        print(f"Total balance: {balance}$")
        self.finalized_assets['total'] = balance
        return self.finalized_assets


if __name__ == "__main__":
    okex = MyOkex()
    print(f'Total balance: {okex.get_balance()}')
