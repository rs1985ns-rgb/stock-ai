import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="AlgoAlpha Powerhouse Pro", layout="wide")
st.title("🔥 AlgoAlpha Powerhouse - Today's Trend Detector")

symbol = st.text_input("Symbol likhein (e.g. BTC-USD, RELIANCE.NS, TSLA):", "BTC-USD")

# --- Advanced Indicators Logic ---
def get_indicators(df):
    # 1. RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 2. SMA (Powerhouse Trend)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    # 3. MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # 4. Today Trend (EMA 9)
    df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
    return df

try:
    df = yf.download(symbol, period="1mo", interval="1h")
    
    if not df.empty:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = get_indicators(df)
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        price = float(last_row['Close'])
        rsi = float(last_row['RSI'])
        macd = float(last_row['MACD'])
        sig = float(last_row['Signal_Line'])
        ema9 = float(last_row['EMA_9'])
        sma20 = float(last_row['SMA_20'])

        # --- Today's Trend Header ---
        trend_color = "green" if price > ema9 else "red"
        st.markdown(f"### Today's Trend: <span style='color:{trend_color}'>{'📈 BULLISH' if price > ema9 else '📉 BEARISH'}</span>", unsafe_allow_html=True)

        # --- Metrics ---
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Current Price", f"${price:,.2f}")
        m2.metric("RSI (14)", f"{rsi:.2f}")
        m3.metric("EMA 9 (Trend)", f"${ema9:,.2f}")
        m4.metric("MACD Status", "Positive" if macd > sig else "Negative")

        # --- AlgoAlpha & Powerhouse Decision Logic ---
        st.divider()
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("🛡️ Powerhouse Signal")
            if price > sma20 and macd > sig and rsi < 70:
                st.success("💎 POWERHOUSE BUY: Price is strong and momentum is building!")
            elif price < sma20 and macd < sig and rsi > 30:
                st.error("⚠️ POWERHOUSE SELL: Trend is breaking down. Exit recommended.")
            else:
                st.info("⚖️ POWERHOUSE: Waiting for confirmation...")

        with col_right:
            st.subheader("🎯 AlgoAlpha Verdict")
            if rsi < 35 and price > prev_row['Low']:
                st.success("🚀 ALGO-BUY: Oversold recovery detected.")
            elif rsi > 65 and price < prev_row['High']:
                st.error("📉 ALGO-SELL: Profit booking zone reached.")
            else:
                st.warning("🔄 ALGO: Neutral / Sideways")

        # --- Chart ---
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Price"))
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_9'], line=dict(color='cyan', width=1), name="EMA 9 (Trend)"))
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], line=dict(color='orange', width=2), name="SMA 20 (Powerhouse)"))
        
        fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False, title=f"Advanced Analysis for {symbol}")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Data load nahi hua. Check symbol.")

except Exception as e:
    st.error(f"Error: {e}")
