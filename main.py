import numpy as np
import matplotlib.pyplot as plt

def calcMA(prices, period):
    return np.mean(prices[-period:])

if __name__ == "__main__":
    prices = []
    base = 100

    for i in range(len(100)):
        trend = prices * .1
        noise = np.random.normal(0, 2)
        price = base + trend + noise
        prices.append(price)
    
    