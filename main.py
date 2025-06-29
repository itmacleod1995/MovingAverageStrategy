import numpy as np
import matplotlib.pyplot as plt

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
        if i - 1 >= short_period:
            sma.append(calcMA(prices[:i], short_period))
        else:
            sma.append(None)  # Not enough data yet
            
        # Calculate Long Moving Average if we have enough data
        if i - 1 >= long_period:
            lma.append(calcMA(prices[:i], long_period))
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
    
    # Plot the moving averages
    plt.plot(sma, label="SMA")
    plt.plot(lma, label="LMA")

    plt.legend()
    plt.show()
        
    return states

if __name__ == "__main__":
    # Generate synthetic price data for testing
    prices = []
    base = 100  # Starting price

    # Create 100 data points with upward trend and random noise
    for i in range(100):
        trend = i * .1  # Linear upward trend
        noise = np.random.normal(0, 2)  # Random noise with mean=0, std=2
        price = base + trend + noise
        prices.append(price)
    
    # Set up the plot
    plt.figure(figsize=(12, 8))
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title("Moving Average Strategy")
    plt.plot(prices, label="Price")

    # Generate trading signals using our strategy
    states = signal(prices)

    plt.legend()
    plt.show()
    
