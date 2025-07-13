import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
from pandas_datareader._utils import RemoteDataError
import datetime as dt
import yfinance as yf
import pandas as pd

def signal(prices, sma, lma):
    """
    Generate trading signals based on moving average crossover strategy.
    
    Strategy: Buy when Short MA crosses above Long MA, Sell when it crosses below.
    
    Args:
        prices (list): List of price values
        short_period (int): Period for Short Moving Average (default: 10)
        long_period (int): Period for Long Moving Average (default: 30)
    
    Returns:
        list: Trading signals - "Buy", "Sell", or "Hold"
    """
    states = []  # Trading signals
    sma_higher = False  # Track if SMA was above LMA in previous period
    sma_crosses_lma = False
    
    for i in range(len(prices)):    
        # Only check for crossovers if i > 0 and all values are not None
        if (
            i > 0 and
            sma[i] is not None and lma[i] is not None and
            sma[i - 1] is not None and lma[i - 1] is not None
        ):
            # Check for a bullish crossover: previous SMA was below or equal to LMA, now it's above
            if sma[i] > lma[i] and sma[i - 1] <= lma[i - 1] and sma_higher == False:
                print("SMA crosses above LMA: SMA = {}, LMA = {}".format(sma[i], lma[i]))
                sma_crosses_lma = True  # Mark that a crossover just occurred
                sma_higher = True
            elif sma[i] < lma[i] and sma[i - 1] >= lma[i - 1] and sma_higher:
                print("SMA crosses below LMA: SMA = {}, LMA = {}".format(sma[i], lma[i]))
                sma_crosses_lma = True
                sma_higher = False
            else:
                sma_crosses_lma = False  # No crossover or not enough data
        else:
            sma_crosses_lma = False  # Not enough data for crossover check

        # Detect bullish crossover: SMA crosses above LMA
        if sma_crosses_lma and sma_higher:
            states.append("Buy")
        # Detect bearish crossover: SMA crosses below LMA
        elif sma_crosses_lma and sma_higher == False:
            states.append("Sell")
        else:
            states.append("Hold")  # No crossover, maintain current position
        
    return states

def backtest(prices, states):
    cash = 1000
    position = 0 #0 = not in the market, 1 is in the market
    portfolio = []
    num_of_shares = 0
    for i in range(len(prices)):
        if states[i] == "Buy" and position == 0:
            #Buy
            position = 1
            num_of_shares = cash / prices[i]
            print("Buy at {}".format(prices[i]))
            cash = 0
        elif states[i] == "Sell" and position == 1:
            #Sell
            position = 0
            print("Sell at {}".format(prices[i]))
            cash = num_of_shares * prices[i]
            num_of_shares = 0
        
        portfolio_val = cash + (num_of_shares * prices[i])
        portfolio.append(portfolio_val)
    
    total = cash + (num_of_shares * prices[-1])

    return portfolio, total

def plot_moving_averages(sma, lma, price):
    # Set up the plot
    plt.figure(figsize=(12, 8))
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.plot(sma, label="SMA")
    plt.plot(lma, label="LMA")
    plt.plot(price, label="Closing Price")

    plt.title("Moving Average Strategy")
    plt.legend()
    plt.grid()

    plt.show()

def plot_portfolio(portfolio):
    plt.figure(figsize=(12,8))
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.plot(portfolio, label="Portfolio Value")

    plt.title("Portfolio Value Over Time")
    plt.legend()
    plt.grid()

    plt.show()

if __name__ == "__main__":
    
    start = dt.datetime(2020, 1, 1)
    end = dt.datetime(2020, 12, 31)
    
    df = yf.download("SPY", start, end)
    if df is None:
        print("None!")
        exit()

    #Calculate SMA and LMA
    df['SMA'] = df['Close'].rolling(10).mean()
    df['LMA'] = df['Close'].rolling(30).mean()
    
    # Generate trading signals using our strategy
    states = signal(df['Close'], df['SMA'], df['LMA'])
    prices = df['Close']['SPY'].to_numpy()
    portfolio_val, total = backtest(prices, states)
    df['Portfolio Value'] = portfolio_val

    plot_moving_averages(df['SMA'], df['LMA'], df['Close'])
    plot_portfolio(df['Portfolio Value'])
    #print("total value = {}".format(total))
    
