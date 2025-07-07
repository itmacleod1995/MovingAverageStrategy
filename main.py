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
    curr_sma_crosses_lma = False
    
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
        
        # Only check for crossovers if i > 0 and all values are not None
        if (
            i > 0 and
            sma[i] is not None and lma[i] is not None and
            sma[i - 1] is not None and lma[i - 1] is not None
        ):
            # Check for a bullish crossover: previous SMA was below or equal to LMA, now it's above
            if sma[i] > lma[i] and sma[i - 1] <= lma[i - 1]:
                print("Small Moving Average = {}, Long Moving Average = {}".format(sma[i], lma[i]))
                curr_sma_crosses_lma = True  # Mark that a crossover just occurred
            else:
                curr_sma_crosses_lma = False  # No crossover or not enough data
        else:
            curr_sma_crosses_lma = False  # Not enough data for crossover check

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
    
    start = dt.datetime(2020, 1, 1)
    end = dt.datetime(2020, 12, 31)
    
    """
    df = yf.download("SPY", start, end)
    if df is None:
        print("None!")

    prices = df['Close']['SPY'].tolist()
    """

    prices = []
    base = 100
    for i in range(80):
        trend = i * .01
        noise = np.random.normal(0, 2)
        price = base + trend + noise
        prices.append(price)


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

    backtest(prices, states)

    plt.show()
    
