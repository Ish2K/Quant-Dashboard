# Quant-Dashboard

## Overview
The **Quant-Dashboard** is an interactive web-based application designed for analyzing stock fundamentals, clustering companies based on financial metrics, and visualizing data insights. This tool uses machine learning techniques to group stocks with similar financials and provides key financial ratios for fundamental analysis.

Key features include:
- **K-Means Clustering**: Group companies with similar financial metrics.
- **Visualization**: Interactive visualizations using Plotly for PCA-based clustering.
- **Fundamental Analysis**: Fetch and display key ratios like PE, PB, ROE, etc., using `yfinance`.
- **Cluster Metrics**: Calculate and display metrics such as average price, median price, and tickers with the highest/lowest stock prices within each cluster.

---

## Features
1. **Fundamental Data Analysis**:
   - Extracts financial ratios like PE ratio, PB ratio, ROE, Debt-to-Equity, and more using `yfinance`.

2. **K-Means Clustering**:
   - Groups companies into clusters based on selected financial metrics.
   - Supports custom PCA components (2D and 3D visualizations).

3. **Cluster Metrics**:
   - Displays aggregated metrics for each cluster:
     - Average stock price.
     - Median stock price.
     - Ticker with the highest and lowest price.

4. **Interactive Visualizations**:
   - Visualize clusters with PCA using Plotly.
   - Analyze clustering results in 2D or 3D.

---

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8 or later
- pip (Python package manager)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ish2K/Quant-Dashboard.git
   cd Quant-Dashboard
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the Script**:
   ```bash
   python main.py
   ```

2. **Enter Stock Tickers**:
   - Input the stock tickers you want to analyze (e.g., AAPL, MSFT, GOOGL).

3. **Interact with the Dashboard**:
   - View fundamental ratios and clustering results.
   - Explore metrics for each cluster (average price, median price, etc.).
   - Use Plotly visualizations for 2D/3D clustering insights.

---

## Example Output

### Fundamental Data:
| Ticker | Market Cap       | PE Ratio | PB Ratio | ROE    | Profit Margin | Current Ratio | Stock Price |
|--------|------------------|----------|----------|--------|---------------|---------------|-------------|
| AAPL   | 2.5T            | 28.1     | 34.2     | 30.5%  | 0.25          | 1.2           | $175.23     |
| MSFT   | 2.4T            | 35.2     | 13.8     | 35.2%  | 0.31          | 2.1           | $325.40     |

### Cluster Metrics:
| Cluster | Average Price | Median Price | Lowest Price Ticker | Lowest Price | Highest Price Ticker | Highest Price |
|---------|---------------|--------------|---------------------|--------------|----------------------|---------------|
| 0       | $120.5        | $115.0       | TICKER_X            | $90.0        | TICKER_Y             | $150.0        |
| 1       | $300.8        | $310.0       | TICKER_Z            | $250.0       | TICKER_W             | $350.0        |

### Visualization:
- Interactive PCA-based clustering visualizations in 2D and 3D.

---

## Configuration
- **Number of Clusters**: Adjust the `n_clusters` parameter in the code to customize the number of K-Means clusters.
- **PCA Components**: Use 2 or 3 components for PCA visualization by modifying the `n_components` parameter in the `visualize_clusters_with_pca` function.

---

## Technologies Used
- **Python**: Core programming language.
- **Libraries**:
  - `yfinance`: Fetching stock financial data.
  - `scikit-learn`: Clustering (K-Means) and dimensionality reduction (PCA).
  - `plotly`: Interactive visualizations.
  - `pandas` and `numpy`: Data manipulation.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing
Contributions are welcome! If you have suggestions, bug fixes, or new features, feel free to submit a pull request.

---

## Contact
For questions or feedback, please contact:
- **Email**: ishaan.gupta04@hotmail.com
- **GitHub**: [ish2k](https://github.com/ish2k)

---

Let me know if you need help with customizations or deployment instructions!