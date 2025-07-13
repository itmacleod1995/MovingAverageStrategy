#import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import pandas_datareader.data as pdr
import yfinance as yf

def load_data(start, end, symbol="SPY"):
    """
    Download historical price data for a given symbol from Yahoo Finance.

    Parameters:
        start (datetime): The start date for the data.
        end (datetime): The end date for the data.
        symbol (str): The ticker symbol to download (default: 'SPY').

    Returns:
        pd.DataFrame: DataFrame containing the historical price data.
    """
    df = yf.download(symbol, start, end)
    if df is None or df.empty:
        print("Error loading data")
        exit()
    return df

