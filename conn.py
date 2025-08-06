import os
from alpaca.trading.client import TradingClient
from dotenv import load_dotenv

def connect():
    load_dotenv()

    key = os.getenv("key")
    secret = os.getenv("API_SECRET")

    trading_client = TradingClient(key, secret, paper=True)
    return trading_client.get_account()


