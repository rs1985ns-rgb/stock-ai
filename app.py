import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="AI Market Signal", layout="wide")
st.title("📈 AI Trading Signal (Master Version)")

symbol = st.text_input("Symbol likhein (e.g. BTC-USD, TSLA, SBIN.NS):", "BTC-USD")

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

try:
    # 1. Download Data
    df = yf.download(symbol, period="1mo", interval="1h")
    
    if not df.empty:
        # Multi-index fix: Agar columns double hain toh unhe single karein
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # 2. RSI Calculation
        df['RSI'] = calculate_rsi(df)
        
        # 3. Get Last Values (Safest Way)
        last_price = float(df['Close'].iloc[-1])
        last_rsi = float(df['RSI'].iloc[-1])

        # 4. Display Metrics
        c1, c2 = st.columns(2)
        c1.metric("Price", f"${last_price:,.2f}")
        c2.metric("RSI", f"{last_rsi:.2f}" if not pd.isna(last_rsi) else "Loading...")

        # 5. Signal Logic
        if last_rsi < 35:
            st.success("🤖 SIGNAL: 🚀 BUY")
        elif last_rsi > 65:
            st.error("🤖 SIGNAL: 📉 SELL")
        else:
            st.info("🤖 SIGNAL: ⚖️ NEUTRAL")

        # 6. Chart
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']
        )])
        fig.update_layout(template="plotly_dark", title=f"{symbol} Chart", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Data nahi mil raha. Symbol sahi likhein.")

except Exception as e:
    st.error(f"Technical Error: {e}")
