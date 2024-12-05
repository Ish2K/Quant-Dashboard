import numpy as np
import riskfolio as rp
import yfinance as yf 
import matplotlib.pyplot as plt 
import pandas as pd 
import streamlit as st
import plotly.graph_objs as go
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


@st.cache_data
def load_data(ticker: str):

    return yf.Ticker(ticker).info

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
    ],
)

calc = cont2.button("Calculate")

if calc:
    fund = Fundamentals(stocks_list, analysis_type)
    data = fund.start_analysis()
    st.write(data)

### ADD KNN MODEL NEXT