import os
import alpaca_trade_api as tradeapi
import config

"""
Establishes connection with api
"""
def connect():
    #load config variables from .env
    key = config.key
    secret = config.secret
    url = config.BASE_URL

    #establish connection
    conn = tradeapi.REST(key, secret, url, api_version="v2")
    return conn



