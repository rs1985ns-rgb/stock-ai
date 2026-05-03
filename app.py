import streamlit as st
import pandas as pd
import json
from urllib.request import urlopen

st.set_page_config(page_title="Market Signals", layout="wide")
st.title("📈 AI Market Signal (Lite Version)")

# Simple Symbol Input
symbol = st.text_input("Symbol (e.g., BTCUSDT, ETHUSDT):", "BTCUSDT")

# Fetching Data using a direct public API (Binance - no extra library needed)
try:
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    response = urlopen(url)
    data = json.loads(response.read())

    price = float(data['lastPrice'])
    change = float(data['priceChangePercent'])

    st.metric("Price", f"${price:,.2f}", f"{change}%")

    if change < -3:
        st.success("🤖 SIGNAL: BUY 🚀 (Market Dip Detected)")
    elif change > 3:
        st.error("🤖 SIGNAL: SELL 📉 (High Profit Booking Zone)")
    else:
        st.info("🤖 SIGNAL: NEUTRAL ⚖️ (Wait for move)")

except Exception as e:
    st.error("Symbol sahi daalein (Sirf Crypto like BTCUSDT, ETHUSDT kaam karega is lite version mein)")
