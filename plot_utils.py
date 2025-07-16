#import dependencies
import matplotlib.pyplot as plt

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