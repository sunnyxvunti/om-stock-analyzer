import yfinance as yf
import numpy as np

def get_stock_data(ticker: str, start: str, end: str):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    if df.empty:
        raise ValueError(f'No data returned for ticker {ticker}')
    df = df[['Close']].copy()
    df.columns = ['Close']
    df.dropna(inplace=True)
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
    return df
