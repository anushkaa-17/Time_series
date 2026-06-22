import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta
from utils.plotly_figure import plotly_table, close_chart, candlestick, RSI, Moving_average, MACD

# setting page config
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="page_with_curl",
    layout="wide",
)

st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)
today = datetime.date.today()

with col1:
    # UPDATED: Replaced st.text_input with st.selectbox for top 6 US companies
    ticker_options = {
        "NVDA": "NVIDIA (NVDA)",
        "MSFT": "Microsoft (MSFT)",
        "AAPL": "Apple (AAPL)",
        "AMZN": "Amazon (AMZN)",
        "GOOGL": "Alphabet (GOOGL)",
        "META": "Meta (META)"
    }
    ticker = st.selectbox(
        'Select Stock Ticker', 
        options=list(ticker_options.keys()), 
        format_func=lambda x: ticker_options[x]
    )
with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", datetime.date(today.year, today.month, today.day))

st.subheader(ticker)
stock = yf.Ticker(ticker)
st.write(stock.info['longBusinessSummary'])
st.markdown("### 🏢 Corporate Information")
st.write(f"**Full-Time Employees:** {stock.info.get('fullTimeEmployees', 'N/A'):,}")
st.write(f"**Headquarters:** {stock.info.get('city', 'N/A')}, {stock.info.get('country', 'N/A')}")
st.write(f"**Exchange:** {stock.info.get('exchange', 'N/A')}")
st.write("**Website:**", stock.info["website"])

st.markdown("### 📊 Key Statistics")

col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index=["Market Cap", "Beta", "EPS", "PE Ratio"])
    df[""] = [
        stock.info["marketCap"],
        stock.info["beta"],
        stock.info["trailingEps"],
        stock.info["trailingPE"],
    ]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

with col2:
    df = pd.DataFrame(
        index=[
            "Revenue per share",
            "Profit Margins",
            "Debt to Equity",
            "Return on Equity",
        ]
    )
    df[""] = [
        stock.info["revenuePerShare"],
        stock.info["profitMargins"],
        stock.info["debtToEquity"],
        stock.info["returnOnEquity"],
    ]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)


data = yf.download(ticker, start=start_date, end=end_date)

# Check if data was returned successfully
if not data.empty and len(data) >= 2:
    col1, col2, col3 = st.columns(3)
    daily_change = data["Close"].iloc[-1] - data["Close"].iloc[-2]
    # Force the values into clean floats/scalars
    last_close = float(data["Close"].iloc[-1].iloc[0]) if isinstance(data["Close"].iloc[-1], pd.Series) else float(data["Close"].iloc[-1])
    change_val = float(daily_change.iloc[0]) if isinstance(daily_change, pd.Series) else float(daily_change)

    col1.metric(
        label="Daily Change",
        value=f"${last_close:.2f}",
        delta=f"{change_val:.2f}"
    )

    last_10_df = data.tail(10).sort_index(ascending=False).round(3)
    last_10_df.columns = [col[0] if isinstance(col, tuple) else col for col in last_10_df.columns]
    fig_df = plotly_table(last_10_df)

    st.write("##### Historical Data (Last 10 days)")
    st.plotly_chart(fig_df, use_container_width=True)
else:
    st.error(f"No stock data found for ticker '{ticker}' within the selected date range.")

col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns([1,1,1,1,1,1,1,1,1,1,1,1])

num_period = ''
with col1:
    if st.button('5D'):
        num_period = '5d'
with col2:
    if st.button('1M'):
        num_period = '1mo'
with col3:
    if st.button('6M'):
        num_period = '6mo'
with col4:
    if st.button('YTD'):
        num_period = 'ytd'
with col5:
    if st.button('1Y'):
        num_period = '1y'
with col6:
    if st.button('5Y'):
        num_period = '5y'
with col7:
    if st.button('MAX'):
        num_period = 'max'

col1, col2, col3 = st.columns([1,1,4])
with col1:
    chart_type = st.selectbox('', ('Candle', 'Line'))
with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('', ('RSI', 'MACD'))
    else:
        indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))

ticker_ = yf.Ticker(ticker)


new_df1 = ticker_.history(period='max')
data1 = ticker_.history(period='max')

if num_period == '':
    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)
        
    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)
        
    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)
        
    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(data1, '1y'), use_container_width=True)
    
    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)
        
else:
    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)
        
    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)
        
    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)
        
    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(new_df1, num_period), use_container_width=True)
        
    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)