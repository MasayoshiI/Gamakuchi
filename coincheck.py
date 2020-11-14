import json
import requests
import time
import hmac
import hashlib
from configparser import ConfigParser, NoSectionError
import argparse
import sys


class Coincheck:
    """ Class for CoinCheck API access it takes Access key and Secret key"""

    def __init__(self, access_key, secret_key, url='https://coincheck.com'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = url

    def get(self, path, params=None):
        """ GET for given path for Coincheck"""
        if params != None:
            params = json.dumps(params)
        else:
            params = ''
        nonce = str(int(time.time()))
        message = nonce + self.url + path + params

        signature = self.getSignature(message)

        return requests.get(
            self.url+path,
            headers=self.getHeader(self.access_key, nonce, signature)
        ).json()

    def post(self, path, params):
        """ POST for given path for Coincheck"""
        params = json.dumps(params)
        nonce = str(int(time.time()))
        message = nonce + self.url + path + params

        signature = self.getSignature(message)

        return requests.post(
            self.url+path,
            data=params,
            headers=self.getHeader(self.access_key, nonce, signature)
        ).json()

    def delete(self, path):
        """ DELETE for given path for Coincheck """
        nonce = str(int(time.time()))
        message = nonce + self.url + path

        signature = self.getSignature(message)

        return requests.delete(
            self.url+path,
            headers=self.getHeader(self.access_key, nonce, signature)
        ).json()

    def getSignature(self, message):
        """get signature """
        signature = hmac.new(
            bytes(self.secret_key.encode('ascii')),
            bytes(message.encode('ascii')),
            hashlib.sha256
        ).hexdigest()

        return signature

    def getHeader(self, access_key, nonce, signature):
        """ get header for API access"""
        headers = {
            'ACCESS-KEY': access_key,
            'ACCESS-NONCE': nonce,
            'ACCESS-SIGNATURE': signature,
            'Content-Type': 'application/json' 
        }

        return headers


    def get_transaction_history(self):
        """Get transaction history"""
        
        path_orders_transactions = '/api/exchange/orders/transactions'
        orders = self.get(path_orders_transactions)
        # print(orders)

        path_orders_transactions_pagination = '/api/exchange/orders/transactions_pagination'
        transaction_page = self.get(path_orders_transactions_pagination)
        
        # print(transaction_page)
        return transaction_page
    
    def get_balance(self):
        """Get balance of coincheck account"""
        
        path_balance = '/api/accounts/balance'
        balance = self.get(path_balance)
        # print(balance)
        
        return balance

    def get_order_books(self):
        """Get order book"""        
        
        path_order_books = '/api/order_books'
        orderbooks = self.get(path_order_books)
        
        return orderbooks

    def print_rates(self):
        """print out Rates at exchange"""
        # key = coin, item = pair
        coins = {'BTC': 'btc_jpy', 'ETH': 'eth_jpy',
         'XEM': 'xem_jpy', 'BCH': 'bch_jpy'}

        path_rates = '/api/rate/'
        
        for key, item in coins.items():
            coincheck = self.get(path_rates+item)
            print(item)
            print("%-4s : %-10s" % (key, coincheck['rate']))

    def get_rate(self, pair):
        """get rate of the given pair"""
        path_rate = '/api/rate/' + pair
        rate = self.get(path_rate)

        return rate

    def order(self, pair, order_type, rate, amount):
        """Order for given pair, order_type, rate and amount"""
        path_orders = '/api/exchange/orders'
        # create params for the order
        params = {
            "pair": pair,
            "order_type": order_type,
            "rate": rate,
            "amount": amount,
        }
        # Order
        order_result = coincheck.post(path_orders, params)
        
        # Show result
        print(order_result)

    def get_unsettled_orders(self):
        """Get the list of unsettled orders"""
        path_unsettled = '/api/exchange/orders/opens'
        unsettled_list = coincheck.get(path_unsettled)
        
        return unsettled_list

    def cancel_order(self, order_num):
        """Cancel the order and print cancelled results"""
        path_order_cancel = '/api/exchange/orders/' + str(order_num)
        cancelled_result = coincheck.delete(path_order_cancel)
        print(cancelled_result)


### TEST CODE HERE ###
config = ConfigParser()
config.read('gamakuchi.conf')

# get keys
access_key = config.get('GamakuchiBot', 'coincheckkey')
secret_key = config.get('GamakuchiBot', 'coinchecksecret')

# Create an instance
coincheck = Coincheck(access_key, secret_key)

#### Check Profile ####
print(coincheck.get_balance())
# print(coincheck.get_transaction_history())
print(coincheck.get_order_books())


