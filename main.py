# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
from pandas_datareader._utils import RemoteDataError
import datetime as dt
import pandas as pd
from data import load_data
from strategy import signal
from backtest import backtest
from indicators import garman_klass
from conn import connect

if __name__ == "__main__":

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)

    # Define the start and end dates for data download
    start = "2020-01-01"
    end = "2020-12-30"

    #connect to alpaca api
    acct = connect()
    #print(acct.get_account().equity)
    
    #Grab historical data via API
    df = load_data(acct, start, end)

    #drop unnecessary columns
    df = df.drop(['trade_count', 'volume', 'vwap'], axis=1)

    # Round closing prices to 2 decimal places for cleaner display
    df['close'] = df['close'].round(2)

    # Calculate short and long moving averages
    # Round MA values to 2 decimal places for consistency
    df['SMA'] = df['close'].rolling(10).mean().round(2)
    df['LMA'] = df['close'].rolling(20).mean().round(2)

    # Extract closing prices as a NumPy array
    prices = df['close'].values

    # Calculate Garman-Klass volatility for each day
    df['volatility'] = garman_klass(df)
    # Round volatility to 2 decimal places for readability
    df['volatility'] = df['volatility'].round(2)
    
    # Generate trading signals using our strategy
    states = signal(prices, df['SMA'], df['LMA'], df['volatility'])

    # Store the generated signals in the DataFrame
    df['Position'] = states

    # Run backtest to simulate trading and get portfolio values
    portfolio_val, total = backtest(prices, states)
    
    # Add portfolio value column to dataframe
    df['Portfolio Value'] = portfolio_val
    # Round portfolio values to 2 decimal places for cleaner display
    df['Portfolio Value'] = df['Portfolio Value'].round(2)

    # Filter DataFrame for buy signals
    buySignals = df[df.Position == "Buy"]

    #Filter DataFrame for sell signals
    sellSignals = df[df.Position == "Sell"]

    #print(df[["close", "SMA", "LMA", "Position", "Portfolio Value"]])
    print("Starting equity = {}, Ending equity = {}".format(10000, np.round(total, 2)))

    print(df[df.Position == "Hold"][["SMA", "LMA", "Position", "volatility"]])

    """Plot"""
    # Set up the plot for price and moving averages
    
    plt.figure(figsize=(12, 8))
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.plot(df['SMA'], label="SMA", color="Orange")
    plt.plot(df['LMA'], label="LMA", color="Purple")
    plt.plot(df['close'], label="Price", color="LightBlue")

    plt.title("Moving Average Crossover Strategy")

    # Overlay buy signals as green upward triangles
    plt.scatter(buySignals.index, buySignals['close'], marker="^", color="darkgreen", label="Buy")

    #Overlay sell signals as red x triangles
    plt.scatter(sellSignals.index, sellSignals['close'], marker="x", color="red", label="Sell")

    plt.grid()
    plt.legend()
    plt.show()
    
    #Plot returns
    plt.figure(figsize=(12,8))
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.plot(df['Portfolio Value'], label="Portfolio Value", color="Green")
    plt.title("Portfolio Value Over Time")
    plt.legend()
    plt.grid()
    plt.show()
    


  

  

    
