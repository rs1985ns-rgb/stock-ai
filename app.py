import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

# Page Config
st.set_page_config(page_title="AI Multi-Market Predictor", layout="wide")

st.title("🤖 AI Market Analyzer (Stocks, Crypto, Gold, Oil)")
st.write("Ye AI market ka data scan karke Buy/Sell signals aur Prediction deta hai.")

# Sidebar - Market Selection
st.sidebar.header("Market Settings")
market_type = st.sidebar.selectbox("Market Chunein:", ["Stock", "Crypto", "Commodity"])

if market_type == "Stock":
    symbol = st.sidebar.text_input("Stock Symbol (e.g., RELIANCE.NS, TSLA):", "RELIANCE.NS")
elif market_type == "Crypto":
    symbol = st.sidebar.text_input("Crypto Symbol (e.g., BTC-USD, ETH-USD):", "BTC-USD")
else:
    symbol = st.sidebar.selectbox("Commodity Chunein:", ["GC=F (Gold)", "CL=F (Crude Oil)", "SI=F (Silver)"])
    if " " in symbol: symbol = symbol.split(" ")[0]

# Fetch Data
@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, period="2y", interval="1d")
    return data

data = load_data(symbol)

if not data.empty:
    # --- CALCULATIONS ---
    # 1. RSI (Buy/Sell Signal)
    data['RSI'] = ta.rsi(data['Close'], length=14)
    
    # 2. Moving Averages
    data['MA20'] = data['Close'].rolling(window=20).mean()
    
    last_price = data['Close'].iloc[-1]
    last_rsi = data['RSI'].iloc[-1]
    prev_price = data['Close'].iloc[-2]
    change = ((last_price - prev_price) / prev_price) * 100

    # --- UI DASHBOARD ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${round(last_price, 2)}", f"{round(change, 2)}%")
    col2.metric("RSI (Momentum)", round(last_rsi, 2))
    
    # AI Logic for Signals
    if last_rsi < 30:
        col3.success("AI SIGNAL: 🔥 STRONG BUY")
    elif last_rsi > 70:
        col3.error("AI SIGNAL: ⚠️ STRONG SELL")
    elif last_price > data['MA20'].iloc[-1]:
        col3.info("AI SIGNAL: 👍 BULLISH HOLD")
    else:
        col3.warning("AI SIGNAL: 👎 BEARISH / WAIT")

    # --- CHARTING ---
    st.subheader(f"{symbol} Visual Analysis")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="Price", line=dict(color='cyan')))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name="Trend (MA20)", line=dict(dash='dash')))
    st.plotly_chart(fig, use_container_width=True)

    # --- AI PREDICTION (Next Day Trend) ---
    st.subheader("🔮 AI Future Trend Prediction")
    if last_price > data['MA20'].iloc[-1] and last_rsi < 60:
        st.write(f"AI Model Analysis: Market trend **Upward** lag raha hai. Agle session mein price badhne ki sambhavna hai.")
    else:
        st.write(f"AI Model Analysis: Market mein thodi **Weakness** hai. Niche ke levels ka intezar karein.")

else:
    st.error("Data nahi mil raha. Kripya sahi symbol check karein.")

st.sidebar.info("Tip: Indian stocks ke liye .NS lagayein (e.g. SBIN.NS)")
