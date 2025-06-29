import numpy as np
import matplotlib.pyplot as plt

def calcMA(prices, period):
    return np.mean(prices[-period:]) 

def signal(prices, short_period = 10, long_period = 30):
    sma = []
    lma = []
    states = []
    sma_higher = False
    for i in range(len(prices)):
        if i - 1 >= short_period:
            sma.append(calcMA(prices[:i], short_period))
        else:
            sma.append(None)
        if i - 1 >= long_period:
            lma.append(calcMA(prices[:i], long_period))
        else:
            lma.append(None)
        
        curr_sma_crosses_lma = sma[i] > lma[i] if sma[i] and lma[i] else False

        if curr_sma_crosses_lma and sma_higher == False:
            sma_higher = True
            states.append("Buy")
        elif curr_sma_crosses_lma == False and sma_higher:
            sma_higher = False
            states.append("Sell")
        else:
            states.append("Hold")
    
    plt.plot(sma, label="SMA")
    plt.plot(lma, label="LMA")

    plt.legend()
    plt.show()
        
    return states

if __name__ == "__main__":
    prices = []
    base = 100

    for i in range(100):
        trend = i * .1
        noise = np.random.normal(0, 2)
        price = base + trend + noise
        prices.append(price)
    
    plt.figure(figsize=(12, 8))
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title("Moving Average Strategy")
    plt.plot(prices, label="Price")

    states = signal(prices)

    plt.legend()

    plt.show()
    
