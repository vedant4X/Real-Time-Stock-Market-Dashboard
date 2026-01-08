import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.title("📈 Real-Time Stock Market Dashboard")

# Sidebar inputs
st.sidebar.header("Stock Selection")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
period = st.sidebar.selectbox(
    "Select Time Period",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"]
)

interval = st.sidebar.selectbox(
    "Select Interval",
    ["1m", "5m", "15m", "30m", "1h", "1d"]
)

@st.cache_data
def load_data(symbol, period, interval):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period, interval=interval)
    return data

try:
    data = load_data(stock_symbol, period, interval)

    if data.empty:
        st.error("No data found. Please check the stock symbol.")
    else:
        st.subheader(f"📌 {stock_symbol.upper()} Stock Price")

        # Line Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Close Price'
        ))

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Price (USD)",
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Show metrics
        latest_price = data['Close'].iloc[-1]
        previous_price = data['Close'].iloc[-2]
        change = latest_price - previous_price
        percent_change = (change / previous_price) * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Price", f"${latest_price:.2f}")
        col2.metric("Change", f"${change:.2f}", f"{percent_change:.2f}%")
        col3.metric("Volume", f"{int(data['Volume'].iloc[-1]):,}")

        # Data Table
        st.subheader("📄 Raw Stock Data")
        st.dataframe(data.tail(20))

except Exception as e:
    st.error(f"Error occurred: {e}")
