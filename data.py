#import dependencies
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import config
import datetime as dt


def load_data(start, end, symbol="SPY"):
    key = config.key
    secret = config.secret
    client = StockHistoricalDataClient(key, secret)

    request = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe = TimeFrame.Day,
        start = start,
        end = end
    )

    bars = client.get_stock_bars(request)

    return bars

