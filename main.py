from bsc import MyBinance
from kcn import MyKucoin
from bybit import MyByBit

if __name__ == '__main__':
    bybit = MyByBit().get_balance()
    print()
    kucoin = MyKucoin().get_balance()
    print()
    binance = MyBinance().get_balance()
    print()
    print(
        f'Total balance from CEXs: {bybit + kucoin + binance}')
