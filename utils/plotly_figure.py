import plotly.graph_objects as go
import dateutil
import pandas_ta as pta
import datetime


def plotly_table(dataframe):
    headerColor = "grey"
    rowEvenColor = "#f8fafd"
    rowOddColor = "#e1efff"

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=["<b></b>"]
                    + ["<b>" + str(i)[:10] + "</b>" for i in dataframe.columns],
                    line_color="#0078ff",
                    fill_color="#0078ff",
                    align="center",
                    font=dict(color="white", size=15),
                    height=35,
                ),
                cells=dict(
                    values=[["<b>" + str(i) + "</b>" for i in dataframe.index]]
                    + [dataframe[i] for i in dataframe.columns],
                    fill_color=[[rowOddColor, rowEvenColor] * len(dataframe)],
                    align="left",
                    line_color=["white"],
                    font=dict(color=["black"], size=15),
                ),
            )
        ]
    )

    dynamic_height = max(150, (len(dataframe) * 35) + 50)

    fig.update_layout(
        height=dynamic_height, 
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

def filter_data(dataframe, num_period):
    if num_period == "1mo":
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == "5d":
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == "6mo":
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == "1y":
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == "5y":
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == "ytd":
        date = datetime.datetime(dataframe.index[-1].year, 1, 1).strftime("%Y-%m-%d")
    else:
        date = dataframe.index[0]

    return dataframe.reset_index()[dataframe.reset_index()["Date"] > date]


def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines', name='Close', line=dict(width=2, color='white')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'], mode='lines', name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], mode='lines', name='Low', line=dict(width=2, color='red')))
    
    # FIX IS HERE: Turn off the range slider explicitly!
    fig.update_xaxes(rangeslider_visible=False, showgrid=True, gridcolor="#222938")
    fig.update_yaxes(showgrid=True, gridcolor="#222938")
    
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#111723",
        paper_bgcolor="#111723",
        font=dict(color="white"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)")
    )
    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dataframe['Date'],
        open=dataframe['Open'],
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close'],
        name="Price"
    ))
    
    fig.update_xaxes(rangeslider_visible=False, showgrid=True, gridcolor="#222938")
    fig.update_yaxes(showgrid=True, gridcolor="#222938")
    
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#111723",
        paper_bgcolor="#111723",
        font=dict(color="white")
    )
    return fig


def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe.RSI, name='RSI', line=dict(width=2, color='orange')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[70]*len(dataframe), name='Overbought', line=dict(width=1.5, color='#ff4a4a', dash='dash')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[30]*len(dataframe), fill='tonexty', name='Oversold', line=dict(width=1.5, color='#2fd67a', dash='dash')))
    
    fig.update_xaxes(showgrid=True, gridcolor="#222938")
    fig.update_yaxes(range=[0, 100], showgrid=True, gridcolor="#222938")
    
    fig.update_layout(
        height=220,
        plot_bgcolor="#111723",
        paper_bgcolor="#111723",
        font=dict(color="white"),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)")
    )
    return fig

def Moving_average(dataframe, num_period):
    dataframe["SMA_50"] = pta.sma(dataframe["Close"], 50)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Open"],
            mode="lines",
            name="Open",
            line=dict(width=2, color="#5ab7ff"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Close"],
            mode="lines",
            name="Close",
            line=dict(width=2, color="black"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["High"],
            mode="lines",
            name="High",
            line=dict(width=2, color="#0078ff"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Low"],
            mode="lines",
            name="Low",
            line=dict(width=2, color="red"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["SMA_50"],
            mode="lines",
            name="SMA_50",
            line=dict(width=2, color="purple"),
        )
    )

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor="white",
        paper_bgcolor="#e1efff",
        legend=dict(yanchor="top", xanchor="right"),
    )

    return fig

def MACD(dataframe, num_period):
    # ... keeping your extraction logic the same ...
    macd = pta.macd(dataframe["Close"]).iloc[:, 0]
    macd_signal = pta.macd(dataframe["Close"]).iloc[:, 1]
    macd_hist = pta.macd(dataframe["Close"]).iloc[:, 2]

    dataframe["MACD"] = macd
    dataframe["MACD Signal"] = macd_signal
    dataframe["MACD Hist"] = macd_hist
    dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    
    # 1. MACD Line
    fig.add_trace(go.Scatter(x=dataframe["Date"], y=dataframe["MACD"], name="MACD", line=dict(width=2, color="#39a1ff")))
    # 2. Signal Line
    fig.add_trace(go.Scatter(x=dataframe["Date"], y=dataframe["MACD Signal"], name="Signal", line=dict(width=1.5, color="#ff4a4a", dash="dash")))
    
    # 3. Add the structural Histogram Bars cleanly
    c = ["#ff4a4a" if cl < 0 else "#2fd67a" for cl in dataframe["MACD Hist"]]
    fig.add_trace(go.Bar(x=dataframe['Date'], y=dataframe['MACD Hist'], marker_color=c, name='Histogram'))

    fig.update_xaxes(showgrid=True, gridcolor="#222938")
    fig.update_yaxes(showgrid=True, gridcolor="#222938")

    fig.update_layout(
        height=250,
        plot_bgcolor="#111723",
        paper_bgcolor="#111723",
        font=dict(color="white"),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)"  # Seamless transparent background
        ),
    )
    return fig

def Moving_average_forecast(forecast):
    fig = go.Figure()

    # Historical Close Price (Updated line color to white for visibility on dark layout)
    fig.add_trace(go.Scatter(
        x=forecast.index[:-30], 
        y=forecast['Close'].iloc[:-30],
        mode='lines',
        name='Close Price', 
        line=dict(width=2, color='white')
    ))

    # Predicted Future Close Price
    fig.add_trace(go.Scatter(
        x=forecast.index[-31:], 
        y=forecast['Close'].iloc[-31:],
        mode='lines',
        name='Future Close Price',
        line=dict(width=2, color='red')
    ))

    # Match axes styling and hide the range slider to keep background changes stable
    fig.update_xaxes(rangeslider_visible=False, showgrid=True, gridcolor="#222938")
    fig.update_yaxes(showgrid=True, gridcolor="#222938")

    # Dark premium background layouts and positioning adjustments
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#111723",
        paper_bgcolor="#111723",
        font=dict(color="white"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)"
        )
    )

    return fig