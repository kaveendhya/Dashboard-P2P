import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Merchant Volume Visualization (Combined Data)", layout="wide")

# Data URLs
url1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdpesJtXBqu31XSP1FNBV5mDyA9Ef28fRB7efObJuyw59n-ZKbpEKajC2gnaGT9iwdL4DEe7UylYls/pub?gid=1261335317&single=true&output=csv"
url2 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSa_DSo1mD5Bf8SrAfw2s2jCEJ4_9jTHL7pMg4Mh-hn8Y5pWZ4GVX3b5dviIaboB5lUrn-QtjJrvGmV/pub?gid=2033676081&single=true&output=csv"

@st.cache_data(show_spinner=False)
def load_and_combine_data(urls):
    dfs = []
    for url in urls:
        df = pd.read_csv(url)
        dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df

# Load data
df = load_and_combine_data([url1, url2])

# Convert 'Max Amt' to numeric (essential fix)
df['Max Amt'] = pd.to_numeric(df['Max Amt'], errors='coerce')
df = df.dropna(subset=['Max Amt'])  # Remove rows where conversion failed

# Parse date and time columns
df['Fetched At'] = pd.to_datetime(df['Fetched At'], errors='coerce')
df = df.dropna(subset=['Fetched At'])

df['Hour'] = df['Fetched At'].dt.hour
df['Date'] = df['Fetched At'].dt.date

# Ensure core columns exist
if 'AdvertiserNick' not in df.columns:
    st.error("Column 'AdvertiserNick' not found in data.")
    st.stop()
if 'Max Amt' not in df.columns:
    st.error("Column 'Max Amt' not found in data.")
    st.stop()

# Sidebar: user input
st.sidebar.title("Settings")
merchant_names = df['AdvertiserNick'].dropna().unique()
selected_merchant = st.sidebar.selectbox("Select Merchant", merchant_names)
aggregation = st.sidebar.radio("Aggregate by", options=["Hourly", "Daily"])

filtered = df[df['AdvertiserNick'] == selected_merchant]

if filtered.empty:
    st.warning(f"No data available for merchant: {selected_merchant}")
    st.stop()

if aggregation == "Hourly":
    grouped = filtered.groupby('Hour')['Max Amt'].mean().sort_index()
    st.header(f"Average Hourly Volume (Max Amt) for: {selected_merchant}")
    st.bar_chart(grouped)
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Max Amt')
    ax.set_title(f"Average Max Amt per Hour ({selected_merchant})")
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)
else:
    grouped = filtered.groupby('Date')['Max Amt'].mean().sort_index()
    st.header(f"Average Daily Volume (Max Amt) for: {selected_merchant}")
    st.line_chart(grouped)
    fig, ax = plt.subplots(figsize=(12, 6))
    grouped.plot(kind='bar', color='cornflowerblue', ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Average Max Amt')
    ax.set_title(f"Average Max Amt per Day ({selected_merchant})")
    plt.xticks(rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)
