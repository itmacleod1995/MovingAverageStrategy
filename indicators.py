import numpy as np
import pandas as pd

def garman_klass(df):
    """
    Calculate Garman-Klass volatility estimator.
    
    This is an improved volatility measure that uses OHLC (Open, High, Low, Close) data
    instead of just close-to-close returns. It provides a more accurate estimate of
    volatility by incorporating intraday price movements.
    
    Formula: σ = √(0.5 * (ln(H/L))² - (2*ln(2) - 1) * (ln(C/O))²)
    
    Args:
        df (pd.DataFrame): DataFrame with 'Open', 'High', 'Low', 'Close' columns
        
    Returns:
        np.array: Volatility estimates (standard deviation, not variance)
    """
    
    # Extract OHLC price data and flatten to 1D arrays
    # .values converts to numpy array, .ravel() flattens to 1D
    close_price = df['close'].values
    open_price = df['open'].values
    high = df['high'].values
    low = df['low'].values

    # Garman-Klass volatility formula:
    # σ = √(0.5 * (ln(H/L))² - (2*ln(2) - 1) * (ln(C/O))²)
    # 
    # Where:
    # - ln(H/L) captures the intraday range (high-low movement)
    # - ln(C/O) captures the open-to-close movement
    # - The coefficients optimize the estimator for accuracy
    # - Final sqrt converts variance to standard deviation (volatility)
    
    return np.sqrt(.5 * (np.log(high / low)) ** 2 - (2 * np.log(2) - 1) * (np.log(close_price / open_price)) ** 2)