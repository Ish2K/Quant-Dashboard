# cache data

from functools import cache
import yfinance as yf
import time
import pandas as pd

@cache
def load_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    return yf.download(ticker, start, end)

def load_stocks_data(tickers: list, start: str, end: str) -> pd.DataFrame:

    df = pd.DataFrame()
    for ticker in tickers:
        try:
            temp_df = (load_stock_data(ticker, '2021-01-01', '2021-12-31')["Close"])
        except:
            temp_df = pd.DataFrame()
        df = pd.concat([df, temp_df], axis=1)
    
    # remove columns with missing data
    df.dropna(axis=1, inplace=True)
    
    return df