import pandas as pd
import numpy as np

def add_indicators(df):
    # Simple Moving Averages
    df['SMA_20'] = df['Close'].rolling(20).mean()
    df['SMA_50'] = df['Close'].rolling(50).mean()

    # Bollinger Bands
    rolling = df['Close'].rolling(20)
    df['BB_Mid']   = rolling.mean()
    df['BB_Upper'] = df['BB_Mid'] + 2 * rolling.std()
    df['BB_Lower'] = df['BB_Mid'] - 2 * rolling.std()

    # RSI
    delta    = df['Close'].diff()
    gain     = delta.clip(lower=0)
    loss     = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs       = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df
