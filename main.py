import numpy as np
import matplotlib.pyplot as plt

def calcMA(prices, period):
    return np.mean(prices[-period:])

def signal(prices, short_period = 10, long_period = 30):
    sma = []
    lma = []
    for i in range(len(prices)):
        if i - 1 >= short_period:
            sma.append(calcMA(prices[:i + 1], short_period))
        

    

    


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

    plt.legend()

    plt.show()
    
