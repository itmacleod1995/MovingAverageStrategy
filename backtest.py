# Function to backtest the strategy and simulate trading
def backtest(prices, states):
    cash = 1000  # Starting cash
    position = 0 # 0 = not in the market, 1 = in the market
    portfolio = []  # Track portfolio value over time
    num_of_shares = 0  # Number of shares held
    for i in range(len(prices)):
        if states[i] == "Buy" and position == 0:
            # Buy if signal is Buy and not already in the market
            position = 1
            num_of_shares = int(cash // prices[i])
            cash = cash - (prices[i] * num_of_shares)
            print("Number of shares = {}".format(num_of_shares))
            #print("Buy at {}".format(prices[i]))
            #cash = 0
        elif states[i] == "Sell" and position == 1:
            # Sell if signal is Sell and currently in the market
            position = 0
            #print("Sell at {}".format(prices[i]))
            cash = cash + (num_of_shares * prices[i])
            num_of_shares = 0
        
        # Calculate current portfolio value (cash + value of held shares)
        portfolio_val = cash + (num_of_shares * prices[i])
        portfolio.append(portfolio_val)
    
    total = cash + (num_of_shares * prices[-1])  # Final portfolio value

    return portfolio, total