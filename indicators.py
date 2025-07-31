import numpy as np
import pandas as pd

def garman_klass(df):
    close_price = df['Close'].values.ravel()
    open_price = df['Open'].values.ravel()
    high = df['High'].values.ravel()
    low = df['Low'].values.ravel()

    return np.sqrt(.5 * (np.log(high / low)) ** 2 - (2 * np.log(2) - 1) * (np.log(close_price / open_price)) ** 2)