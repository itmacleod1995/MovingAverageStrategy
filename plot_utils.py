# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

# Function to plot buy and sell signals on the price chart
def plot_signals(df):
    # Filter buy and sell signals from the DataFrame
    buy_signals = df[df.Position == "Buy"]
    sell_signals = df[df.Position == "Sell"]

    # Plot buy signals as green upward triangles
    plt.scatter(buy_signals.index, buy_signals['Close'].to_numpy(), marker="^", color="green", label="Buy", s=100)
    # Plot sell signals as red downward triangles
    plt.scatter(sell_signals.index, sell_signals['Close'].to_numpy(), marker="v", color="red", label="Sell", s=100)


    

