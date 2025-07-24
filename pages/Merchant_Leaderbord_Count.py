import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- SETTINGS ---
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT7oX5g-gdNvqodJEY1H_8LVsbtzC2gpVgpvf0rjlhPmzgXpicwzPLSY7u0D4_78t5YZcjQU08_bAG3/pub?gid=0&single=true&output=csv"
st.set_page_config(page_title="Merchant Daily Leaderboard", layout="centered")

st.title("📊 Merchant Leaderboard by Average Volume")

# --- LOAD DATA ---
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df = df.dropna(subset=["Fetched At", "AdvertiserNick"])
    df["Fetched At"] = pd.to_datetime(df["Fetched At"], errors="coerce")
    if "Average Volume" in df.columns:
        df["Average Volume"] = pd.to_numeric(df["Average Volume"], errors="coerce")
    df["Date"] = df["Fetched At"].dt.date.astype(str)
    return df

df = load_data(csv_url)

# --- SIDEBAR: Date Selection Only ---
available_dates = sorted(df["Date"].unique())
selected_date = st.sidebar.selectbox("Select Date", available_dates, index=len(available_dates) - 1)

# --- MAIN: Only Average Volume Leaderboard ---
filtered = df[df["Date"] == selected_date].copy()
filtered = filtered.dropna(subset=["Average Volume"])

if filtered.empty:
    st.warning(f"No data available for {selected_date}")
else:
    filtered = filtered.sort_values("Average Volume", ascending=False)
    fig = go.Figure(go.Bar(
        x=filtered["Average Volume"],
        y=filtered["AdvertiserNick"],
        orientation="h",
        marker_color="teal"
    ))
    fig.update_layout(
        title=f"Merchant Leaderboard by Average Volume ({selected_date})",
        xaxis_title="Average Volume",
        yaxis_title="Merchant Nickname",
        height=600,
        yaxis=dict(categoryorder="total ascending")
    )
    st.plotly_chart(fig, use_container_width=True)

