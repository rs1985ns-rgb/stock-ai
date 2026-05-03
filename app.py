import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="AI Market Signal Pro", layout="wide")
st.title("📈 AI Trading Signal (RSI + Moving Average)")

symbol = st.text_input("Symbol likhein (e.g. BTC-USD, TSLA, SBIN.NS):", "BTC-USD")

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

try:
    df = yf.download(symbol, period="1mo", interval="1h")
    
    if not df.empty:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # 1. Calculations (RSI + 20 SMA)
        df['RSI'] = calculate_rsi(df)
        df['SMA20'] = df['Close'].rolling(window=20).mean() # Moving Average
        
        last_price = float(df['Close'].iloc[-1])
        last_rsi = float(df['RSI'].iloc[-1])
        last_sma = float(df['SMA20'].iloc[-1])

        # 2. Display Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Price", f"${last_price:,.2f}")
        c2.metric("RSI", f"{last_rsi:.2f}")
        c3.metric("20-SMA Line", f"${last_sma:,.2f}")

        # 3. Smart Signal Logic (Double Confirmation)
        st.subheader("🤖 AI Analysis")
        if last_rsi < 40 and last_price > last_sma:
            st.success("🚀 STRONG BUY: RSI low hai aur Price Recovery mode mein hai (Above SMA).")
        elif last_rsi > 60 and last_price < last_sma:
            st.error("📉 STRONG SELL: RSI high hai aur Price niche gir raha hai (Below SMA).")
        elif last_rsi < 30:
            st.warning("⚡ OVERSOLD: Price sasta hai, lekin trend ka intezar karein.")
        elif last_rsi > 70:
            st.warning("⚠️ OVERBOUGHT: Price mahanga hai, kabhi bhi gir sakta hai.")
        else:
            st.info("⚖️ NEUTRAL: Abhi koi clear signal nahi hai.")

        # 4. Professional Chart
        fig = go.Figure()
        # Candlesticks
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Market"))
        # Moving Average Line
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], line=dict(color='yellow', width=1.5), name="20-Day SMA"))
        
        fig.update_layout(template="plotly_dark", title=f"{symbol} Trend Analysis", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Data nahi mila.")

except Exception as e:
    st.error(f"Technical Error: {e}")
