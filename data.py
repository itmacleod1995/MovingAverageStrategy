#import dependencies
import alpaca_trade_api as tradeapi
import config
import datetime as dt


def load_data(api, start, end, symbol="SPY"):
    data = api.get_bars(symbol, "1Day", start, end).df
    return data
    


