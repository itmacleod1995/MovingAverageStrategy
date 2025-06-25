import numpy as np
import matplotlib.pyplot as plt

def calcMA(prices, period):
    return np.mean(prices[-period:])

if __name__ == "__main__":
    pass