import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go

st.set_page_config(page_title="AI Market Signals", layout="wide")
st.title("📈 AI Market Analyzer")

# User Input
symbol = st.text_input("Symbol (e.g., BTC-USD, RELIANCE.NS, GC=F):", "BTC-USD")

# Data Fetching
data = yf.download(symbol, period="6mo", interval="1d")

if not data.empty:
    # Basic AI Signal Logic (RSI)
    data['RSI'] = ta.rsi(data['Close'], length=14)
    last_price = data['Close'].iloc[-1]
    last_rsi = data['RSI'].iloc[-1]

    # Display Metrics
    col1, col2 = st.columns(2)
    col1.metric("Current Price", f"{last_price:.2f}")
    col2.metric("RSI (Momentum)", f"{last_rsi:.2f}")

    # Buy/Sell Logic
    if last_rsi < 35:
        st.success("🤖 AI SIGNAL: 🚀 BUY (Stock is cheap/Oversold)")
    elif last_rsi > 65:
        st.error("🤖 AI SIGNAL: 📉 SELL (Stock is expensive/Overbought)")
    else:
        st.info("🤖 AI SIGNAL: ⚖️ NEUTRAL (Hold/Wait)")

    # Charting
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
    fig.update_layout(title=f"{symbol} Price Chart", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Data nahi mil raha. Kripya sahi symbol check karein.")
