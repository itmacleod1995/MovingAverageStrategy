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

# Function to backtest the strategy and simulate trading
def backtest(prices, states):
    cash = 1000  # Starting cash
    position = 0 # 0 = not in the market, 1 = in the market
    portfolio = []  # Track portfolio value over time
    num_of_shares = 0  # Number of shares held
    for i in range(len(prices)):
        if states[i] == "Buy" and position == 0:
            # Buy if signal is Buy and not already in the market
            position = 1
            num_of_shares = cash / prices[i]
            print("Buy at {}".format(prices[i]))
            cash = 0
        elif states[i] == "Sell" and position == 1:
            # Sell if signal is Sell and currently in the market
            position = 0
            print("Sell at {}".format(prices[i]))
            cash = num_of_shares * prices[i]
            num_of_shares = 0
        
        # Calculate current portfolio value (cash + value of held shares)
        portfolio_val = cash + (num_of_shares * prices[i])
        portfolio.append(portfolio_val)
    
    total = cash + (num_of_shares * prices[-1])  # Final portfolio value

    return portfolio, total

# Function to plot moving averages and closing price
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

# Function to plot portfolio value over time
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

    start = dt.datetime(2018, 1, 1)
    end = dt.datetime(2020, 12, 31)
    
    df = load_data(start, end)

    # Calculate short and long moving averages
    df['SMA'] = df['Close'].rolling(10).mean()
    df['LMA'] = df['Close'].rolling(30).mean()

    prices = df['Close']['SPY'].to_numpy()
    
    # Generate trading signals using our strategy
    states = signal(prices, df['SMA'], df['LMA'])

    # Run backtest to simulate trading and get portfolio values
    portfolio_val, total = backtest(prices, states)
    df['Portfolio Value'] = portfolio_val

    # Plot moving averages and closing price
    plot_moving_averages(df['SMA'], df['LMA'], df['Close'])
    # Plot portfolio value over time
    plot_portfolio(df['Portfolio Value'])
    
