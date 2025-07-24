import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import math

# 🔁 Auto-refresh every 30 minutes
st_autorefresh(interval=1800000, key="auto_refresh")

# Page settings
st.set_page_config(page_title="Live P2P Buy Depth Chart", layout="centered")
st.title("📈 Binance P2P Buy Depth Chart")

# Time range selector
range_hours = st.selectbox("Select time range:", [1, 6, 24], index=0)

# 📥 Load Google Sheet as CSV
csv_url = "https://docs.google.com/spreadsheets/d/1_E7129svQRn1ySjBwOMKxU0tyMAKfZyF3_NyKxtAgPE/gviz/tq?tqx=out:csv&gid=2033676081"
df = pd.read_csv(csv_url)

# 🧹 Clean and convert data
df = df.dropna(subset=["Fetched At", "Price", "Available Qty"])
df["Fetched At"] = pd.to_datetime(df["Fetched At"])
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Available Qty"] = pd.to_numeric(df["Available Qty"], errors="coerce")

# 🕒 Filter by time range
now = df["Fetched At"].max()
range_start = now - timedelta(hours=range_hours)
df = df[df["Fetched At"] >= range_start]

# 📊 Prepare buy depth data (no filtering by Trade Type)
buy_df = df[["Price", "Available Qty"]].dropna()
buy_df = buy_df.sort_values(by="Price", ascending=True)
buy_df["Cumulative"] = buy_df["Available Qty"].cumsum()

# 📈 Plot only if data is available
if not buy_df.empty:
    min_price = buy_df["Price"].min()
    max_price = buy_df["Price"].max()
    max_volume = math.ceil(buy_df["Cumulative"].max() / 100000) * 100000

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=buy_df["Price"],
        y=buy_df["Cumulative"],
        name="Buy Depth (USDT available)",
        mode="lines",
        fill="tozeroy",
        line=dict(color="green")
    ))

    fig.update_layout(
        title=f"P2P Buy Depth Chart – Last {range_hours} Hour(s)",
        xaxis_title="Price (LKR)",
        yaxis_title="Cumulative USDT Volume",
        xaxis_range=[max_price + 2, min_price - 2],  # Reversed X-axis: Prices from left to right
        yaxis_range=[0, max_volume],
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ No data found for the selected time range.")
