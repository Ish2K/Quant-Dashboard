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


@st.cache_data
def load_data(ticker: str):

    return yf.Ticker(ticker).info

url = r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(url) # Returns list of all tables on page
df = tables[0]
stocks = df['Symbol'].values.tolist()

st.subheader("Fundamental Data:")

options = st.multiselect("Select Stocks For Portfolio", stocks)

df = pd.read_csv('sample.csv')

filter = st.radio("Filter Columns:", ("All","Custom"))
df.set_index('symbol',inplace=True)

if filter == "Custom":
    columns = st.multiselect("Columns:",sorted(df.columns))
else:
    columns = df.columns

if(st.button("Get Fundamental Data")):
    
    infos = []
    for tick in options:
        infos.append(load_data(tick))
    infos = pd.DataFrame(infos)
    # print(infos)
    infos = infos.set_index('symbol')
    st.write(infos[list(set(infos.columns) & set(columns))])


st.info('''
Note: If your selected columns are not displayed, it is because the data is not available for the selected stock.
'''
)