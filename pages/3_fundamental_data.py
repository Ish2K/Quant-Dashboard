import numpy as np
import riskfolio as rp
import yfinance as yf 
import matplotlib.pyplot as plt 
import pandas as pd 
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import quantstats as qs
import warnings
import datetime 
warnings.filterwarnings("ignore")

from neuralprophet import NeuralProphet
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from pylab import plt, mpl
plt.style.use('seaborn-v0_8-whitegrid')
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'serif'
np.set_printoptions(precision=5, suppress=True,formatter={'float': lambda x: f'{x:6.3f}'})
import yfinance as yf

from utils.interpretations import fundamentals_info
from utils.fundamentals import Fundamentals

from config import fundamental_columns
from sklearn.decomposition import PCA

@st.cache_data
def load_data(ticker: str):

    return yf.Ticker(ticker).info

def visualize_clusters_with_pca(df, clusters, n_components=2):
    """
    Visualize clusters using PCA and Plotly.

    Parameters:
    df (pd.DataFrame): Original data with financial metrics.
    clusters (array): Cluster labels.
    n_components (int): Number of PCA components.
    """
    # Apply PCA
    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(df.select_dtypes(include=["float64", "int64"]))

    # Add PCA results and clusters to the DataFrame
    for i in range(n_components):
        df[f"pca{i+1}"] = pca_result[:, i]
    df["cluster"] = clusters

    # Visualization
    if n_components == 2:
        fig = px.scatter(
            df,
            x="pca1",
            y="pca2",
            color=df["cluster"].astype(str),
            hover_data=["ticker"],
            title=f"K-Means Clustering of Stocks (2D PCA)",
            labels={"color": "Cluster"},
        )
    elif n_components == 3:
        fig = px.scatter_3d(
            df,
            x="pca1",
            y="pca2",
            z="pca3",
            color=df["cluster"].astype(str),
            hover_data=["ticker"],
            title=f"K-Means Clustering of Stocks (3D PCA)",
            labels={"color": "Cluster"},
        )
    else:
        # If more than 3 components, just print explained variance
        explained_variance = pca.explained_variance_ratio_
        print(f"Explained Variance by PCA Components: {explained_variance}")

        # Return only the transformed data
        return explained_variance, pca_result

    fig.update_layout(
        title_font_size=20,
        legend_title="Cluster",
    )

    return fig

url = r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(url) # Returns list of all tables on page
df = tables[0]
stocks = df['Symbol'].values.tolist()

st.subheader("Fundamental Data:")

with st.expander("View Fundamental Data Info"):
    fundamentals_info()

cont1 = st.container(border=True)
cont1.markdown("### Fetch Fundamental Data")
col1, col2 = cont1.columns(2)

options = col1.multiselect("Select Stocks For Portfolio", stocks)

df = pd.read_csv('sample.csv')

filter = col2.radio("Filter Columns:", ("All","Custom"))
df.set_index('symbol',inplace=True)

if filter == "Custom":
    columns = cont1.multiselect("Columns:",sorted(df.columns))
else:
    columns = df.columns

if(cont1.button("Get Fundamental Data")):
    
    infos = []
    for tick in options:
        infos.append(load_data(tick))
    infos = pd.DataFrame(infos)
    # print(infos)
    infos = infos.set_index('symbol')
    st.write(infos[list(set(infos.columns) & set(columns))])

cont1.info('''
Note: If your selected columns are not displayed, it is because the data is not available for the selected stock.
'''
)

cont2 = st.container(border=True)
cont2.markdown("### Fundamental Analysis")

col3, col4 = cont2.columns(2)

stocks_list = col3.multiselect("Select Stocks For Portfolio", stocks, key="fundamentals")

analysis_type = col4.selectbox(
    "Fundamentals Metrics",
    options=[
        "Piotroski Score",
        "K-Means Clustering",
    ],
)

if(analysis_type == "K-Means Clustering"):
    k_means_columns_filter = cont2.radio("Filter Columns:", ("All","Custom"), key="k_means")
    if k_means_columns_filter == "Custom":
        k_means_columns = cont2.multiselect("Columns:",sorted(fundamental_columns))
    else:
        k_means_columns = "All"
    
    n_clusters = cont2.number_input("Number of Clusters", min_value=2, max_value=10, value=3)
    n_components = cont2.number_input("Number of Components", min_value=2, max_value=10, value=3)

calc = cont2.button("Calculate")

if calc:
    
    if analysis_type == "Piotroski Score":
        fund = Fundamentals(stocks_list, analysis_type)
        data = fund.start_analysis()
        st.write(data)
    elif analysis_type == "K-Means Clustering":
        
        fund = Fundamentals(stocks_list, analysis_type, custom_columns=k_means_columns, n_clusters=n_clusters, n_components=n_components)
        data = fund.start_analysis()
        fig = visualize_clusters_with_pca(data['raw_data'], data['cluster_labels'], n_components)

        if(n_components > 3):
            st.write("More than 3 components are not supported for visualization.")
            st.write(f"Explained Variance by PCA Components: {fig[0]}")
            st.write("Transformed Data:")
            st.write(fig[1])
        else:
            st.plotly_chart(fig)

        st.write(data['cluster_metrics'])

### ADD KNN MODEL NEXT