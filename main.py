import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
from pandas_datareader._utils import RemoteDataError
import datetime as dt
import yfinance as yf

def calcMA(prices, period):
    """
    Calculate the moving average for a given period.
    
    Args:
        prices (list): List of price values
        period (int): Number of periods for the moving average
    
    Returns:
        float: The average of the last 'period' prices
    """
    return np.mean(prices[-period:]) 

def signal(prices, short_period = 10, long_period = 30):
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
    sma = []  # Short Moving Average values
    lma = []  # Long Moving Average values
    states = []  # Trading signals
    sma_higher = False  # Track if SMA was above LMA in previous period
    
    for i in range(len(prices)):
        # Calculate Short Moving Average if we have enough data
        if i + 1 >= short_period:
            sma.append(calcMA(prices[:i + 1], short_period))
        else:
            sma.append(None)  # Not enough data yet
            
        # Calculate Long Moving Average if we have enough data
        if i + 1 >= long_period:
            lma.append(calcMA(prices[:i + 1], long_period))
        else:
            lma.append(None)  # Not enough data yet
        
        # Check if SMA is currently above LMA (with safety check for None values)
        curr_sma_crosses_lma = sma[i] > lma[i] if sma[i] and lma[i] else False

        # Detect bullish crossover: SMA crosses above LMA
        if curr_sma_crosses_lma and sma_higher == False:
            sma_higher = True
            states.append("Buy")
        # Detect bearish crossover: SMA crosses below LMA
        elif curr_sma_crosses_lma == False and sma_higher:
            sma_higher = False
            states.append("Sell")
        else:
            states.append("Hold")  # No crossover, maintain current position
        
    return states, sma, lma

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
    
    final_val = cash + (num_of_shares * prices[-1])
    print("Total profit: {}".format(final_val - 1000))

   



if __name__ == "__main__":
    
    #start = dt.datetime(2020, 1, 1)
    #end = dt.datetime(2020, 12, 31)
    
    df = yf.download("MSFT")
    print(df)

    prices = df['Close']
    

    # Generate trading signals using our strategy
    states, sma, lma = signal(prices)

    # Set up the plot
    plt.figure(figsize=(12, 8))
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title("Moving Average Strategy")
    plt.plot(prices, label="Price")
    plt.plot(sma, label="Small Moving Average")
    plt.plot(lma, label="Large Moving Average")

    plt.legend()
    plt.grid()
    plt.show()

    backtest(prices, states)
    
