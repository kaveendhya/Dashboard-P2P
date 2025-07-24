import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import streamlit as st

# URLs to load data
url1 = "https://docs.google.com/spreadsheets/d/1Z117FLjmqdfxHzCD5fBbbfq6iOauUSVlzmYehE3FrzM/export?format=csv&gid=1261335317"
url2 = "https://docs.google.com/spreadsheets/d/1_E7129svQRn1ySjBwOMKxU0tyMAKfZyF3_NyKxtAgPE/export?format=csv&gid=2033676081"

# Load data from URLs
df1 = pd.read_csv(url1, low_memory=False)
df2 = pd.read_csv(url2, low_memory=False)

# Merge the data from both sheets
df_all = pd.concat([df1, df2], ignore_index=True)

# Preprocessing steps
df_all['Fetched At'] = pd.to_datetime(df_all['Fetched At'])
df_all = df_all.sort_values('Fetched At').reset_index(drop=True)

# Drop rows with missing critical values
df_all = df_all.dropna(subset=['Fetched At', 'AdvertiserNick'])

# Create 'Day of the Week' column (e.g., Monday, Tuesday, etc.)
df_all['DayOfWeek'] = df_all['Fetched At'].dt.strftime('%A')

# Create 'Hour' column for time-based analysis
df_all['Hour'] = df_all['Fetched At'].dt.hour

# Streamlit app setup
st.title('Merchant Activity Dashboard')

# Select merchant
unique_merchants = df_all['AdvertiserNick'].unique()
selected_merchant = st.selectbox('Select Merchant:', unique_merchants)

# Select time period
time_period = st.selectbox('Select Time Period:', ['Last Week', 'Last Month'])

# Filter data based on time period
def filter_data_by_period(df_all, period='Last Week'):
    today = datetime.today()
    if period == 'Last Week':
        past_date = today - timedelta(days=7)
    elif period == 'Last Month':
        past_date = today - timedelta(days=30)
    
    return df_all[df_all['Fetched At'] >= past_date]

# Filtered data for the selected merchant and time period
df_filtered = filter_data_by_period(df_all, period=time_period)
df_merchant = df_filtered[df_filtered['AdvertiserNick'] == selected_merchant]

# ----- Chart 1: Average Online Appearance Bar Chart -----
def plot_average_online_appearance(df, merchant):
    merchant_data = df[df['AdvertiserNick'] == merchant]
    hourly_counts = merchant_data.groupby('Hour').size().reset_index(name='Count')
    avg_hourly_count = hourly_counts.groupby('Hour')['Count'].mean().reset_index(name='Avg Count')
    
    fig = px.bar(avg_hourly_count, x='Hour', y='Avg Count', 
                 title=f"Average Online Appearance per Hour for {merchant} ({time_period})",
                 labels={'Avg Count': 'Average Appearances', 'Hour': 'Hour of Day'})
    st.plotly_chart(fig)

# ----- Chart 2: Heatmap - Average Online Activity -----
def plot_heatmap_activity(df, merchant):
    merchant_data = df[df['AdvertiserNick'] == merchant]
    
    # Group by 'DayOfWeek' and 'Hour', and count the appearances
    hourly_day_counts = merchant_data.groupby(['DayOfWeek', 'Hour']).size().reset_index(name='Count')
    
    # Calculate the average count for each (DayOfWeek, Hour) combination
    avg_hourly_day_count = hourly_day_counts.groupby(['DayOfWeek', 'Hour'])['Count'].mean().reset_index(name='Avg Count')
    
    # Pivot the data: DayOfWeek = rows, Hour = columns, Avg Count = values
    heatmap_data = avg_hourly_day_count.pivot(index='DayOfWeek', columns='Hour', values='Avg Count')
    
    # Reorder days to start from Monday
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.loc[ordered_days]
    
    # Plot the heatmap
    fig = px.imshow(heatmap_data,
                    labels=dict(x="Hour of Day", y="Day of Week", color="Average Ad Count"),
                    title=f"Average Online Activity for {merchant} ({time_period})",
                    color_continuous_scale="RdBu")
    st.plotly_chart(fig)

# ----- Chart 3: Co-Online Merchants Bar Chart -----
def plot_co_online_merchants(df, merchant):
    # Get the timestamps when the selected merchant was online
    merchant_times = df[df['AdvertiserNick'] == merchant]['Fetched At'].unique()
    
    # Find other merchants who were online at the same time as the selected merchant
    co_online_merchants = df[df['Fetched At'].isin(merchant_times) & (df['AdvertiserNick'] != merchant)]
    
    # Count how many times each merchant appeared online with the selected merchant
    co_appearances = co_online_merchants.groupby('AdvertiserNick').size().reset_index(name='Co-appearances')
    co_appearances = co_appearances.sort_values('Co-appearances', ascending=False)
    
    # Plot the results
    fig = px.bar(co_appearances, x='Co-appearances', y='AdvertiserNick', orientation='h', 
                 title=f"Co-Online Merchants with {merchant} ({time_period})",
                 labels={'Co-appearances': 'Co-appearances', 'AdvertiserNick': 'Merchant'})
    st.plotly_chart(fig)

# Display the charts
if selected_merchant:
    plot_average_online_appearance(df_filtered, selected_merchant)
    plot_heatmap_activity(df_filtered, selected_merchant)
    plot_co_online_merchants(df_filtered, selected_merchant)
