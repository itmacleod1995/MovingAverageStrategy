#import dependencies
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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


    

