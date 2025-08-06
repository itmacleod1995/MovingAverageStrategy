#import dependencies
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from dotenv import load_dotenv
import os
import datetime as dt


def load_data(start, end, symbol="SPY"):
    load_dotenv()
    key = os.getenv("key")
    secret = os.getenv("API_SECRET")
    client = StockHistoricalDataClient(key, secret)

    request = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe = TimeFrame.Day,
        start = start,
        end = end
    )

    bars = client.get_stock_bars(request)

    return bars

