import json
import requests
import time
import hmac
import hashlib
from configparser import ConfigParser, NoSectionError
import argparse
import sys




class Coincheck:
    def __init__(self, access_key, secret_key, url='https://coincheck.com'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = url

    def get(self, path, params=None):
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
        nonce = str(int(time.time()))
        message = nonce + self.url + path

        signature = self.getSignature(message)

        return requests.delete(
            self.url+path,
            headers=self.getHeader(self.access_key, nonce, signature)
        ).json()

    def getSignature(self, message):
        signature = hmac.new(
            bytes(self.secret_key.encode('ascii')),
            bytes(message.encode('ascii')),
            hashlib.sha256
        ).hexdigest()

        return signature

    def getHeader(self, access_key, nonce, signature):
        headers = {
            'ACCESS-KEY': access_key,
            'ACCESS-NONCE': nonce,
            'ACCESS-SIGNATURE': signature,
            'Content-Type': 'application/json' # 超重要。
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
        balance = coincheck.get(path_balance)
        # print(balance)
        return balance

    
        
config = ConfigParser()
config.read('gamakuchi.conf')

# set up api keys
access_key = config.get('GamakuchiBot', 'coincheckkey')
secret_key = config.get('GamakuchiBot', 'coinchecksecret')

# print(access_key)
# print(secret_key)

# Create an instance
coincheck = Coincheck(access_key, secret_key)

#### Check Profile ####
print(coincheck.get_balance())
print(coincheck.get_transaction_history())

##### TODO :
##### BUY order ####
##### SELL order ####
##### Cancel Order ####

