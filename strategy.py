# Function to generate trading signals based on moving average crossovers
def signal(prices, sma, lma):
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
    states = []  # List to store trading signals
    sma_higher = False  # Track if SMA was above LMA in previous period
    sma_crosses_lma = False  # Track if a crossover just occurred
    
    for i in range(len(prices)):
        # Only check for crossovers if i > 0 and all values are not None
        if (
            i > 0 and
            sma[i] is not None and lma[i] is not None and
            sma[i - 1] is not None and lma[i - 1] is not None
        ):
            # Check for a bullish crossover: previous SMA was below or equal to LMA, now it's above
            if sma[i] > lma[i] and sma[i - 1] <= lma[i - 1] and sma_higher == False:
                #print("SMA crosses above LMA: SMA = {}, LMA = {}".format(sma[i], lma[i]))
                sma_crosses_lma = True  # Mark that a crossover just occurred
                sma_higher = True
            # Check for a bearish crossover: previous SMA was above or equal to LMA, now it's below
            elif sma[i] < lma[i] and sma[i - 1] >= lma[i - 1] and sma_higher:
                #print("SMA crosses below LMA: SMA = {}, LMA = {}".format(sma[i], lma[i]))
                sma_crosses_lma = True
                sma_higher = False
            else:
                sma_crosses_lma = False  # No crossover or not enough data
        else:
            sma_crosses_lma = False  # Not enough data for crossover check

        # Detect bullish crossover: SMA crosses above LMA
        if sma_crosses_lma and sma_higher:
            states.append("Buy")
        # Detect bearish crossover: SMA crosses below LMA
        elif sma_crosses_lma and sma_higher == False:
            states.append("Sell")
        else:
            states.append("Hold")  # No crossover, maintain current position
        
    return states