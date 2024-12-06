import pandas as pd
from .load_data import fetch_financial_data
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


class Fundamentals:

    def __init__(self, tickers: list, analysis_type: str = "Piotroski", custom_columns: str | list = "All"
                 , n_clusters: int = 3, n_components: int = 3):
        self.tickers = tickers
        self.analysis_type = analysis_type
        self.custom_columns = custom_columns
        self.n_clusters = n_clusters
        self.n_components = n_components
    
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

    def preprocess_data(self, df):
        """
        Preprocess financial data for clustering.

        Parameters:
        df (pd.DataFrame): Financial data.

        Returns:
        pd.DataFrame, pd.DataFrame: Raw data, scaled data.
        """
        # Drop rows with missing values
        df = df.dropna()

        # Scale numeric features
        numeric_features = df.select_dtypes(include=["float64", "int64"]).columns
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df[numeric_features])

        return df, pd.DataFrame(df_scaled, columns=numeric_features)

    def apply_kmeans(self, data_scaled, n_clusters):
        """
        Apply K-Means clustering to scaled data.

        Parameters:
        data_scaled (pd.DataFrame): Scaled data.
        n_clusters (int): Number of clusters.

        Returns:
        KMeans, array: Fitted KMeans model, cluster labels.
        """
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(data_scaled)
        return kmeans, clusters
    
    def compute_k_means_cluster_metrics(self) -> dict:
        """
        Compute cluster metrics for each cluster.

        Parameters:
        raw_data (pd.DataFrame): Raw data with financial metrics and cluster labels.

        Returns:
        pd.DataFrame: Cluster metrics.
        """

        # Fetch financial data
        financial_data = self.get_fundamentals()

        # set key as ticker

        financial_data = pd.DataFrame(financial_data).T
        financial_data['ticker'] = financial_data.index

        # store last price and ticker
        last_price = financial_data[['ticker', 'Last Price']]

        if(self.custom_columns != "All"):
            financial_data = financial_data[self.custom_columns]

        # remove last price from the data if it is present
        if 'Last Price' in financial_data.columns:
            financial_data = financial_data.drop(columns = ['Last Price'])

        # Preprocess data
        raw_data, scaled_data = self.preprocess_data(financial_data)
        raw_data["ticker"] = financial_data.index

        # Apply K-Means clustering
        
        kmeans_model, cluster_labels = self.apply_kmeans(scaled_data, n_clusters=self.n_clusters)

        # Add clusters to original data
        raw_data["cluster"] = cluster_labels

        # join the last price and ticker to the raw data
        raw_data = raw_data.merge(last_price, left_on = 'ticker', right_on = 'ticker')

        cluster_metrics = pd.DataFrame()

        # get mean last price for each cluster, median last price for each cluster, number of stocks in each cluster, highest last price for each cluster, and lowest last price for each cluster
        cluster_metrics['mean_last_price'] = raw_data.groupby('cluster')['Last Price'].mean()
        cluster_metrics['median_last_price'] = raw_data.groupby('cluster')['Last Price'].median()
        cluster_metrics['num_stocks'] = raw_data.groupby('cluster')['Last Price'].count()
        cluster_metrics['highest_last_price'] = raw_data.groupby('cluster')['Last Price'].max()
        cluster_metrics['lowest_last_price'] = raw_data.groupby('cluster')['Last Price'].min()

        # get ticker with lowest last price for each cluster, ticker with highest last price for each cluster

        cluster_metrics['ticker_highest_last_price'] = raw_data.groupby('cluster')['Last Price'].idxmax().apply(lambda x: raw_data.loc[x, 'ticker'])
        cluster_metrics['ticker_lowest_last_price'] = raw_data.groupby('cluster')['Last Price'].idxmin().apply(lambda x: raw_data.loc[x, 'ticker'])

        return {
            "raw_data": raw_data,
            "cluster_metrics": cluster_metrics,
            "n_components": self.n_components,
            "cluster_labels": cluster_labels
        }

    
    def start_analysis(self):
        if self.analysis_type == "Piotroski Score":
            return self.calculate_piotroski_score_util()
        elif self.analysis_type == "K-Means Clustering":
            return self.compute_k_means_cluster_metrics()
