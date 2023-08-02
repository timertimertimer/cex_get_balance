import os
import telebot
from telebot import types
from config import envs
from bsc import MyBinance
from kcn import MyKucoin
from bybit import MyByBit
from okex import MyOkex

bot = telebot.TeleBot(
    os.getenv('CEX_GET_BALANCE_BOT_TOKEN') or envs['CEX_GET_BALANCE_BOT_TOKEN'], parse_mode=None)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(types.KeyboardButton("/get_balance"))

@bot.message_handler(commands=['get_balance'])
def get_balance(message):
    print('Counting...')
    bybit = MyByBit().get_balance()
    kucoin = MyKucoin().get_balance()
    binance = MyBinance().get_balance()
    okex = MyOkex().get_balance()
    cexs = {
        'Binance': binance,
        'Kucoin': kucoin,
        'ByBit': bybit,
        'OKX': okex,
    }
    balance = 0
    for cex_name, cex_assets in cexs.items():
        s = cex_name.upper() + '\n'
        for ticker, value in cex_assets.items():
            if ticker != 'total':
                amount = value['amount']
                total_usd = value['total']        
                s += f'{ticker} {amount} = {total_usd:.2f}$\n'
            else:
                s += f'Total balance - {value:.2f}$'
                balance += value
        bot.send_message(message.chat.id, s)
    bot.send_message(message.chat.id, f'Total balance from CEXs - {balance:.2f}$', reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling()
