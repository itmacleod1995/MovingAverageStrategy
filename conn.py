import os
from alpaca.trading.client import TradingClient
import config

def connect():

    key = config.key
    secret = config.secret

    trading_client = TradingClient(key, secret, paper=True)
    return trading_client.get_account()


