import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="AI Market Signal", layout="wide")
st.title("📈 AI Trading Signal (Final Fixed)")

# Input Box
symbol = st.text_input("Stock ya Crypto symbol (e.g. BTC-USD, TSLA, RELIANCE.NS):", "BTC-USD")

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

try:
    # 1. Data Download
    data = yf.download(symbol, period="1mo", interval="1h")
    
    if not data.empty:
        # 2. RSI Calculation
        data['RSI'] = calculate_rsi(data)
        
        # 3. Fixing the 'Series' Error - Ekdum Safe Tarika
        # Hum data ki last value ko force karke single number bana rahe hain
        last_price = float(data['Close'].values[-1])
        last_rsi = float(data['RSI'].values[-1])

        # 4. Display Metrics
        col1, col2 = st.columns(2)
        col1.metric("Current Price", f"${last_price:,.2f}")
        
        if pd.isna(last_rsi):
            col2.warning("RSI Calculation pending...")
        else:
            col2.metric("RSI (Momentum)", f"{last_rsi:.2f}")

        # 5. Buy/Sell Logic
        if not pd.isna(last_rsi):
            if last_rsi < 35:
                st.success("🤖 AI SIGNAL: 🚀 BUY (Oversold)")
            elif last_rsi > 65:
                st.error("🤖 AI SIGNAL: 📉 SELL (Overbought)")
            else:
                st.info("🤖 AI SIGNAL: ⚖️ NEUTRAL")

        # 6. Chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Market Data"
        )])
        fig.update_layout(template="plotly_dark", title=f"{symbol} Live Chart", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Data nahi mila. Symbol check karein (Example: TSLA).")

except Exception as e:
    st.error(f"Technical Error: {e}")
