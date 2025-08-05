import os
from alpaca_trade_api import TradingClient
from dotenv import load_dotenv

def connect():
    load_dotenv()

    key = os.getenv("key")
    secret = os.getenv("API_SECRET")

    trading_client = TradingClient(key, secret, paper=True)
    return trading_client


