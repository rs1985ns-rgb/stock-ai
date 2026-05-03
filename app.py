import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="AI Market Signal", layout="wide")
st.title("📈 AI Trading Signal (Bulletproof Version)")

# Input Box
symbol = st.text_input("Stock ya Crypto symbol (e.g. BTC-USD, RELIANCE.NS, TSLA):", "BTC-USD")

# RSI Calculation Formula (No Library Needed)
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

try:
    # Data Fetching
    data = yf.download(symbol, period="1mo", interval="1h")
    
    if not data.empty:
        # RSI nikalna
        data['RSI'] = calculate_rsi(data)
        last_price = float(data['Close'].iloc[-1])
        last_rsi = float(data['RSI'].iloc[-1])

        # Metrics Display
        col1, col2 = st.columns(2)
        col1.metric("Current Price", f"${last_price:,.2f}")
        col2.metric("RSI (Momentum)", f"{last_rsi:.2f}")

        # Buy/Sell Logic
        if last_rsi < 30:
            st.success("🤖 AI SIGNAL: 🚀 BUY (Oversold Zone)")
        elif last_rsi > 70:
            st.error("🤖 AI SIGNAL: 📉 SELL (Overbought Zone)")
        else:
            st.info("🤖 AI SIGNAL: ⚖️ NEUTRAL (Wait)")

        # Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Market Data"
        )])
        fig.update_layout(title=f"{symbol} Live Chart", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Data nahi mila. Kripya symbol sahi se check karein (Example: BTC-USD).")

except Exception as e:
    st.error(f"Kuch galat hua: {e}")
