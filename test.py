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

# generate the client
binance_client = Client(binance_key, binance_secret)

# get every price
prices = binance_client.get_all_tickers()
print(prices)


