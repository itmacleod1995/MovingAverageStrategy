# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
from pandas_datareader._utils import RemoteDataError
import datetime as dt
import yfinance as yf
import pandas as pd
from data import load_data
from strategy import signal
from backtest import backtest
from plot_utils import plot_moving_averages, plot_portfolio, plot_signals

if __name__ == "__main__":

    start = dt.datetime(2018, 1, 1)
    end = dt.datetime(2020, 12, 31)
    
    df = load_data(start, end)

    # Calculate short and long moving averages
    df['SMA'] = df['Close'].rolling(10).mean()
    df['LMA'] = df['Close'].rolling(30).mean()

    prices = df['Close']['SPY'].to_numpy()
    
    # Generate trading signals using our strategy
    states = signal(prices, df['SMA'], df['LMA'])

    df['Position'] = states

    # Run backtest to simulate trading and get portfolio values
    portfolio_val, total = backtest(prices, states)
    df['Portfolio Value'] = portfolio_val

    buySignals = df[df.Position == "Buy"]


    """"Plot"""
    plt.figure(figsize=(15, 10))
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.plot(df['SMA'], label="SMA", color="Orange")
    plt.plot(df['LMA'], label="LMA", color="Purple")
    plt.plot(df['Close'], label="Price", color="LightBlue")

    plt.title("Moving Average Crossover Strategy")

    plt.scatter(buySignals.index, buySignals['Close'], marker="^", color="darkgreen", label="Buy")

    plt.grid()
    plt.legend()
    plt.show()

  


    
