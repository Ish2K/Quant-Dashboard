import pandas as pd
from .load_data import fetch_financial_data

class Fundamentals:

    def __init__(self, tickers: list, analysis_type: str = "Piotroski"):
        self.tickers = tickers
        self.analysis_type = analysis_type
    
    def get_fundamentals(self) -> dict:
        """
        Get the fundamentals for the given tickers.
        """
        fundamentals = {}
        for ticker in self.tickers:
            fundamentals[ticker] = fetch_financial_data(ticker)
        return fundamentals
    
    def calculate_piotroski_score(self, financials):
        """
        Calculate the Piotroski Score based on a company's financial data.

        Parameters:
        financials (dict): Dictionary containing the following keys:
            - net_income (float): Net income of the company.
            - operating_cash_flow (float): Operating cash flow of the company.
            - roa_current (float): Return on assets (ROA) for the current year.
            - roa_previous (float): Return on assets (ROA) for the previous year.
            - leverage_current (float): Current year's leverage (debt-to-equity ratio).
            - leverage_previous (float): Previous year's leverage (debt-to-equity ratio).
            - current_ratio_current (float): Current ratio for the current year.
            - current_ratio_previous (float): Current ratio for the previous year.
            - shares_outstanding_current (float): Current year's number of shares outstanding.
            - shares_outstanding_previous (float): Previous year's number of shares outstanding.
            - gross_margin_current (float): Current year's gross margin.
            - gross_margin_previous (float): Previous year's gross margin.
            - asset_turnover_current (float): Current year's asset turnover ratio.
            - asset_turnover_previous (float): Previous year's asset turnover ratio.

        Returns:
        int: Piotroski Score (range: 0 to 9)
        """
        score = 0
        profitability_score = 0
        leverage_score = 0
        operating_efficiency_score = 0
        pe_ratio = 0

        # Profitability signals
        if financials['net_income'] > 0:
            profitability_score += 1  # Positive net income
        if financials['operating_cash_flow'] > 0:
            profitability_score += 1  # Positive operating cash flow
        if financials['operating_cash_flow'] > financials['net_income']:
            profitability_score += 1  # Operating cash flow > net income
        if financials['roa_current'] > financials['roa_previous']:
            profitability_score += 1  # ROA improvement

        # Leverage, Liquidity, and Source of Funds signals
        if financials['leverage_current'] < financials['leverage_previous']:
            leverage_score += 1  # Decreased leverage
        if financials['current_ratio_current'] > financials['current_ratio_previous']:
            leverage_score += 1  # Improved current ratio
        if financials['shares_outstanding_current'] <= financials['shares_outstanding_previous']:
            leverage_score += 1  # No dilution of shares

        # Operating Efficiency signals
        if financials['gross_margin_current'] > financials['gross_margin_previous']:
            operating_efficiency_score += 1  # Improved gross margin
        if financials['asset_turnover_current'] > financials['asset_turnover_previous']:
            operating_efficiency_score += 1  # Improved asset turnover ratio
        
        pe_ratio = financials['PE Ratio']

        return {
            "Profitablity": profitability_score,
            "Leverage": leverage_score,
            "Operating Efficiency": operating_efficiency_score,
            "PE Ratio": pe_ratio,
            "Piotroski Score" : profitability_score + leverage_score + operating_efficiency_score
        }
    
    def calculate_piotroski_score_util(self) -> pd.DataFrame:
        """
        Calculate the Piotroski Score for the given tickers.

        Returns:
        pd.DataFrame: DataFrame containing the Piotroski Scores for the tickers.
        """
        fundamentals = self.get_fundamentals()
        piotroski_scores = {}
        for ticker, financials in fundamentals.items():
            piotroski_scores[ticker] = self.calculate_piotroski_score(financials)
        
        df = pd.DataFrame(piotroski_scores).T
        df = df[['PE Ratio', 'Profitablity', 'Leverage', 'Operating Efficiency', 'Piotroski Score']]
        return df

    def start_analysis(self):
        if self.analysis_type == "Piotroski Score":
            return self.calculate_piotroski_score_util()
        else:
            return None
    
    ############################################################################################################
    # Add KNN model for predicting stock prices based on fundamentals
    ############################################################################################################
