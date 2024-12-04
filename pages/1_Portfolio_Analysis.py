
import datetime as dt
import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit_shadcn_ui as ui
from PIL import Image
from utils.interpretations import metric_info, var_info, optimization_strategies_info, appinfo
from utils.portfolio_optimizer import PortfolioOptimizer
from utils.metrics import MetricsCalculator
from utils.risk import RiskMetrics

@st.cache_data
def get_stocks_list(url):
    
    tables = pd.read_html(url) # Returns list of all tables on page
    df = tables[0]
    stocks = df.Symbol.values.tolist()
    return stocks

def main():
    im = Image.open("./media/EfficientFrontier.png")

    # st.set_page_config(page_title="Portfolio Optimization Dashboard", page_icon=im)

    st.markdown("## Portfolio Optimization Dashboard")
    
    appinfo()

    with st.expander("View Optimization Strategies"):
        optimization_strategies_info()

    # Using sidebar for inputs

    if "stocks" not in st.session_state:
        st.session_state.stocks_list = ["TSLA", 'NVDA', 'MSFT']  # Initialize empty list

    default_tickers_str = ", ".join(st.session_state.stocks_list)

    cont1 = st.container(border=True)
    cont1.markdown("### Input Parameters")
    
    stocks = get_stocks_list(r"https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")

    # select multiple stocks
    stocks = cont1.multiselect(
        "Select Stocks",
        options=stocks,
        format_func=lambda x: x,
    )
    start, end = cont1.columns(2)
    start_date = start.date_input(
        "Start Date",
        max_value=dt.date.today() - dt.timedelta(days=1),
        min_value=dt.date.today() - dt.timedelta(days=1250),
        value=dt.date.today() - dt.timedelta(days=365),
    )
    end_date = end.date_input(
        "End Date",
        max_value=dt.date.today(),
        min_value=start_date + dt.timedelta(days=1),
        value=dt.date.today(),
    )
    col1, col2 = cont1.columns(2)
    optimization_criterion = col1.selectbox(
        "Optimization Objective",
        options=[
            "Maximize Sharpe Ratio",
            "Minimize Volatility",
            "Maximize Sortino Ratio",
            "Minimize Tracking Error",
            "Maximize Information Ratio",
            "Minimize Conditional Value-at-Risk",
        ],
    )
    riskFreeRate_d = col2.number_input(
        "Risk Free Rate (%)",
        min_value=0.00,
        max_value=100.00,
        step=0.001,
        format="%0.3f",
        value=6.880,
        help = "10 Year Bond Yield"
    )
    calc = cont1.button("Calculate")
    riskFreeRate = riskFreeRate_d / 100

    st.session_state.stocks_list = stocks[:]

    if calc:
        try:
            with st.spinner("Buckle Up! Financial Wizardry in Progress...."):
                stocks_list = st.session_state.stocks_list
                optimizer = PortfolioOptimizer(
                    stocks_list,
                    start_date,
                    end_date,
                    optimization_criterion,
                    riskFreeRate,
                )
                optimizer.optimized_allocation.index = [
                    stock.replace("", "")
                    for stock in optimizer.optimized_allocation.index
                ]
                missing_tickers = False
                ret, std = optimizer.basicMetrics()
                if not (len(ret.columns) == len(stocks_list)):
                    missing_tickers = set(stocks_list) - set(ret.columns)
                    missing_tickers = [str(ticker) for ticker in missing_tickers]
                    # raise ValueError(
                    #     f"Data for the following tickers could not be retrieved: {', '.join(missing_tickers)}"
                    # )

                optimizer.optimized_allocation.columns = ["Allocation (%)"]
                optimizer.optimized_allocation["Allocation (%)"] = [
                    round(i * 100, 2)
                    for i in optimizer.optimized_allocation["Allocation (%)"]
                ]

                metrics = MetricsCalculator(
                    stocks_list,
                    start_date,
                    end_date,
                    optimization_criterion,
                    riskFreeRate,
                )
                
                metric_df = metrics.metricDf()
                metric_df = pd.DataFrame(list(metric_df.items()))
                metric_df.columns = ["Metric", "Value"]

                riskM = RiskMetrics(
                    stocks_list,
                    start_date,
                    end_date,
                    optimization_criterion,
                    riskFreeRate,
                )
        except Exception as e:
            raise ValueError(str(e))
        
        if missing_tickers:
            st.info(f"Data for the following tickers could not be retrieved: {', '.join(missing_tickers)}")

        # except ValueError as e:
        #     print(str(e))
        #     st.error("Unable to download data for one or more tickers!")
        #     return
        # except Exception as e:
        #     st.error(str(e))
        #     return

        with st.container(border=True):
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                [
                    "Summary",
                    "Efficient Frontier",
                    "Metrics",
                    "Portfolio Returns",
                    "Risk Analysis",
                ]
            )
            with tab1:
                st.markdown("#### Optimized Portfolio Performance")
                col1, col2 = st.columns(2)
                col1.markdown(f"**Returns**: {optimizer.optimized_returns}%")
                col1.markdown(f"**Volatility**: {optimizer.optimized_std}%")
                sharpe = (
                    optimizer.optimized_returns - (optimizer.riskFreeRate * 100)
                ) / optimizer.optimized_std
                col1.markdown(f"**Sharpe Ratio**: {round(sharpe, 2)}")
                col1.markdown(f"**Sortino Ratio**: {round(metrics.MSortinoRatio(), 2)}")
                col2.markdown(f"**Time Period**: {(end_date - start_date).days} days")
                st.markdown("#### Optimized Portfolio Allocation")
                alocCol, pieCol = st.columns(2)
                with alocCol:
                    allocations = optimizer.optimized_allocation
                    allocations["Tickers"] = allocations.index
                    allocations = allocations[["Tickers", "Allocation (%)"]]
                    ui.table(allocations)
                with pieCol:
                    sharpeChart = optimizer.optimized_allocation[
                        optimizer.optimized_allocation["Allocation (%)"] != 0
                    ]
                    fig = px.pie(
                        sharpeChart, values="Allocation (%)", names=sharpeChart.index
                    )
                    fig.update_layout(
                        width=180,
                        height=200,
                        showlegend=False,
                        margin=dict(t=20, b=0, l=0, r=0),
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with tab2:
                st.markdown("#### Efficient Frontier Assets")
                frontierAssets, matrix = optimizer.frontierStats()
                ui.table(frontierAssets)
                st.markdown("#### Asset Correlations")
                ui.table(matrix)
                st.markdown("*(Higher Value Represents Higher Correlation)*")
                st.markdown("#### Efficient Frontier Graph")
                optimizer.EF_graph()

            with tab3:
                st.markdown("#### Risk and Return Metrics")
                ui.table(metric_df)
                with st.expander("Metric Interpretations:"):
                    metric_info()

            with tab4:
                st.markdown("#### Cumulative Portfolio Returns")
                metrics.portfolioReturnsGraph()

            with tab5:
                st.markdown("#### VaR and CVaR")
                var = riskM.riskTable()
                ui.table(var)
                with st.expander("VaR and CVar Interpretation"):
                    var_info()
                st.markdown("#### VaR Breaches")
                riskM.varXReturns()


if __name__ == "__main__":
    main()
