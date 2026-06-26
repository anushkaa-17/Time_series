import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
from utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_best_arima_params, inverse_scaling, fit_model
import pandas as pd
from datetime import datetime, timedelta
from utils.plotly_figure import plotly_table, Moving_average_forecast

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_downwards_trend",
    layout="wide",
)

st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)

with col1:
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

st.subheader('Predicting Next 30 days Close Price for: ' + ticker)

# Load and prepare data
close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)

with st.spinner("Optimizing ARIMA parameters and generating forecast..."):

    best_p, best_q, scaled_rmse = get_best_arima_params(scaled_data, differencing_order)
    
    # Multiplying by the scaler's scale factor converts standard deviation back to dollars
    true_dollar_rmse = round(scaled_rmse * scaler.scale_[0], 2)
    

    predictions_scaled = fit_model(scaled_data, best_p, differencing_order, best_q)

st.success(f"Optimal parameters found: ARIMA({best_p}, {differencing_order}, {best_q})")
st.write("**Model True RMSE Score:** $", true_dollar_rmse)


start_date = datetime.now().strftime("%Y-%m-%d")
end_date = (datetime.now() + timedelta(days=29)).strftime("%Y-%m-%d")
forecast_index = pd.date_range(start=start_date, end=end_date, freq="D")

forecast = pd.DataFrame(predictions_scaled, index=forecast_index, columns=["Close"])
forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

# Display forecast table
st.write('##### Forecast Data (Next 30 days)')
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

# Combine for visualization chart
if isinstance(rolling_price.columns, pd.MultiIndex):
    rolling_price.columns = rolling_price.columns.get_level_values(0)

combined_forecast = pd.concat([rolling_price, forecast])
st.plotly_chart(Moving_average_forecast(combined_forecast.iloc[150:]), use_container_width=True)