import urllib
import json
import time
import hmac
import hashlib
from binance.enums import *
from configparser import ConfigParser, NoSectionError
import argparse
import sys
import requests


from binance.client import Client

config = ConfigParser()
config.read('gamakuchi.conf')

# set up api key
binance_key = config.get('GamakuchiBot','binancekey')
binance_secret = config.get('GamakuchiBot','binanceSecret')
coincheck_key = config.get('GamakuchiBot', 'coincheckkey')
coincheck_secret = config.get('GamakuchiBot', 'coinchecksecret')


######### PYPL #############
# from coincheck import order, market, account
# o1 = order.Order(secret_key=coincheck_secret, access_key=coincheck_key)
# print(o1.history())


# m1 = market.Market()
# print(m1.ticker())

# print(m1.trades())

### Ticker ###
URL = 'https://coincheck.com/api/ticker'
coincheck = requests.get(URL).json() 
for key, item in coincheck.items():
    print("%-9s : %-10.9s " % (key, item))


#### Trades ###
URL = 'https://coincheck.com/api/trades'
coincheck = requests.get(URL, params={"offset": 20}).json() 
print(coincheck)

#### Order Book ####
URL = 'https://coincheck.com/api/order_books'
coincheck = requests.get(URL).json() 
for key in coincheck.keys():
    print(key, ":")
    for value in coincheck[key]:
        print(value)
    print()

#### Rates ####
URL = 'https://coincheck.com/api/exchange/orders/rate'
params = {'order_type': 'sell', 'pair': 'btc_jpy', 'amount': 0.1}
coincheck = requests.get(URL, params=params).json() 
print(coincheck)

params = {'order_type': 'buy', 'pair': 'btc_jpy', 'price': 280000}
coincheck = requests.get(URL, params=params).json() 
print(coincheck)

#### Rate Pair ####
coins = {'BTC': 'btc_jpy', 'ETH': 'eth_jpy',
         'XEM': 'xem_jpy', 'BCH': 'bch_jpy'}

URL = 'https://coincheck.com/api/rate/'

for key, item in coins.items():
    coincheck = requests.get(URL+item).json()
    print("%-4s : %-10s" % (key, coincheck['rate']))

    


