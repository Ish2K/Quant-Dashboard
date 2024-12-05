# cache data

from functools import cache
import yfinance as yf
import time
import pandas as pd

@cache
def load_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Load stock data for a given ticker.

    Parameters:
        ticker (str): The stock ticker symbol (e.g., "AAPL" for Apple).
        start (str): The start date in "YYYY-MM-DD" format.
        end (str): The end date in "YYYY-MM-DD" format.
    
    Returns:
        pd.DataFrame: A DataFrame containing the stock data.
    """
    return yf.download(ticker, start, end)

@cache
def fetch_financial_data(ticker):
    """
    Fetch financial data for a given ticker using yfinance.

    Parameters:
    ticker (str): The stock ticker symbol (e.g., "AAPL" for Apple).

    Returns:
    dict: A dictionary containing the financial metrics required for Piotroski Score.
    """
    # Fetch the company data
    stock = yf.Ticker(ticker)
    
    # Income statement
    income_stmt = stock.financials
    # print(income_stmt.T.columns)
    net_income = income_stmt.loc["Net Income"].iloc[0]  # Most recent net income
    net_income_prev = income_stmt.loc["Net Income"].iloc[1]  # Previous year's net income
    
    # Cash flow statement
    cashflow = stock.cashflow
    # print(cashflow.T.columns)
    operating_cash_flow = cashflow.loc["Cash Flow From Continuing Operating Activities"].iloc[0]  # Current OCF
    operating_cash_flow_prev = cashflow.loc["Cash Flow From Continuing Operating Activities"].iloc[1]  # Previous OCF
    
    # Balance sheet
    balance_sheet = stock.balance_sheet
    # print(balance_sheet.T.columns)
    total_assets = balance_sheet.loc["Total Assets"].iloc[0]  # Current year total assets
    total_assets_prev = balance_sheet.loc["Total Assets"].iloc[1]  # Previous year total assets
    total_liabilities = balance_sheet.loc["Total Liabilities Net Minority Interest"].iloc[0]  # Current liabilities
    total_liabilities_prev = balance_sheet.loc["Total Liabilities Net Minority Interest"].iloc[1]  # Previous liabilities
    current_assets = balance_sheet.loc["Current Assets"].iloc[0]
    current_liabilities = balance_sheet.loc["Current Liabilities"].iloc[0]
    current_assets_prev = balance_sheet.loc["Current Assets"].iloc[1]
    current_liabilities_prev = balance_sheet.loc["Current Liabilities"].iloc[1]
    shares_outstanding = stock.info['sharesOutstanding']
    
    # Calculations
    roa_current = net_income / total_assets  # Current ROA
    roa_previous = net_income_prev / total_assets_prev  # Previous ROA
    leverage_current = total_liabilities / total_assets  # Current leverage
    leverage_previous = total_liabilities_prev / total_assets_prev  # Previous leverage
    current_ratio_current = current_assets / current_liabilities
    current_ratio_previous = current_assets_prev / current_liabilities_prev
    gross_margin_current = income_stmt.loc["Gross Profit"].iloc[0] / income_stmt.loc["Total Revenue"].iloc[0]
    gross_margin_previous = income_stmt.loc["Gross Profit"].iloc[1] / income_stmt.loc["Total Revenue"].iloc[1]
    asset_turnover_current = income_stmt.loc["Total Revenue"].iloc[0] / total_assets
    asset_turnover_previous = income_stmt.loc["Total Revenue"].iloc[1] / total_assets_prev

    # Compile data into a dictionary
    financials = {
        "net_income": net_income,
        "operating_cash_flow": operating_cash_flow,
        "roa_current": roa_current,
        "roa_previous": roa_previous,
        "leverage_current": leverage_current,
        "leverage_previous": leverage_previous,
        "current_ratio_current": current_ratio_current,
        "current_ratio_previous": current_ratio_previous,
        "shares_outstanding_current": shares_outstanding,
        "shares_outstanding_previous": shares_outstanding,  # Assuming no dilution data from yfinance
        "gross_margin_current": gross_margin_current,
        "gross_margin_previous": gross_margin_previous,
        "asset_turnover_current": asset_turnover_current,
        "asset_turnover_previous": asset_turnover_previous,
        "PE Ratio": stock.info['trailingPE'],
    }
    return financials

def load_stocks_data(tickers: list, start: str, end: str) -> pd.DataFrame:
    """
    Load stock data for a list of tickers.

    Parameters:
        tickers (list): A list of stock ticker symbols.
        start (str): The start date in "YYYY-MM-DD" format.
        end (str): The end date in "YYYY-MM-DD" format.
    
    Returns:
        pd.DataFrame: A DataFrame containing the closing prices of the stocks.
    """

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

