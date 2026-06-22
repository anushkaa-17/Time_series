import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
from utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_best_arima_params, inverse_scaling, get_forecast
import pandas as pd
from utils.plotly_figure import plotly_table, Moving_average_forecast

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_downwards_trend",
    layout="wide",
)

st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    # Dictionary mapping ticker symbols to company names for clarity
    ticker_options = {
        "NVDA": "NVIDIA (NVDA)",
        "MSFT": "Microsoft (MSFT)",
        "AAPL": "Apple (AAPL)",
        "AMZN": "Amazon (AMZN)",
        "GOOGL": "Alphabet (GOOGL)",
        "META": "Meta (META)"
    }
    
    # The dropdown menu selector
    ticker = st.selectbox(
        'Select Stock Ticker', 
        options=list(ticker_options.keys()), 
        format_func=lambda x: ticker_options[x]
    )

rmse = 0

st.subheader('Predicting Next 30 days Close Price for: ' + ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)

with st.spinner("Optimizing ARIMA parameters..."):
    best_p, best_q, rmse = get_best_arima_params(scaled_data, differencing_order)

st.success(f"Optimal parameters found: ARIMA({best_p}, {differencing_order}, {best_q})")

st.write("**Model RMSE Score:**", rmse)

forecast = get_forecast(scaled_data, differencing_order)

forecast['Close'] = inverse_scaling(scaler, forecast['Close'])
st.write('##### Forecast Data (Next 30 days)')
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)


if isinstance(rolling_price.columns, pd.MultiIndex):
    rolling_price.columns = rolling_price.columns.get_level_values(0)

forecast = pd.concat([rolling_price, forecast])

st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), use_container_width=True)