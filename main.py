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
from indicators import garman_klass

if __name__ == "__main__":
    # Define the start and end dates for data download
    start = dt.datetime(2020, 1, 1)
    end = dt.datetime(2021, 1, 1)
    
    # Load historical price data using the data module
    df = load_data(start, end, "SPY")

    # Calculate short and long moving averages
    df['SMA'] = df['Close'].rolling(10).mean()
    df['LMA'] = df['Close'].rolling(20).mean()

    # Extract closing prices as a NumPy array and convert to 1-D array
    prices = df['Close'].values.ravel()

    df['Volatility'] = garman_klass(df)
    
    # Generate trading signals using our strategy
    states = signal(prices, df['SMA'], df['LMA'])

    # Store the generated signals in the DataFrame
    df['Position'] = states

    # Run backtest to simulate trading and get portfolio values
    portfolio_val, total = backtest(prices, states)
    #df['Portfolio Value'] = portfolio_val

    # Filter DataFrame for buy signals
    buySignals = df[df.Position == "Buy"]

    #Filter DataFrame for sell signals
    sellSignals = df[df.Position == "Sell"]

    print(df.head())
    exit()

    """Plot"""
    # Set up the plot for price and moving averages
    plt.figure(figsize=(12, 8))
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.plot(df['SMA'], label="SMA", color="Orange")
    plt.plot(df['LMA'], label="LMA", color="Purple")
    plt.plot(df['Close'], label="Price", color="LightBlue")

    plt.title("Moving Average Crossover Strategy")

    # Overlay buy signals as green upward triangles
    plt.scatter(buySignals.index, buySignals['Close'], marker="^", color="darkgreen", label="Buy")

    #Overlay sell signals as red x triangles
    plt.scatter(sellSignals.index, sellSignals['Close'], marker="x", color="red", label="Sell")

    plt.grid()
    plt.legend()
    plt.show()

  

  

    
