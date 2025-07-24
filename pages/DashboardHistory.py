import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Load data
df = pd.read_csv("daily_converted_data.csv")
df['Day'] = pd.to_datetime(df['Day'])
df['BTC vs LKR Interpolated'] = df['BTC vs LKR'].interpolate(method='linear')

# Prepare data for chart
df['Date'] = df['Day']

# Cap Premium function
def cap_premium(df):
    df = df[df['Day'] >= '2021-11-01']
    cap = df['P2P Premium'].quantile(0.995)
    df['Premium Capped'] = df['P2P Premium'].clip(upper=cap)
    return df

# Define a function to prepare data for different timeframes
def prepare_data(tf, col1, col2=None, capped=False):
    df_copy = cap_premium(df.copy()) if capped else df
    
    if tf == "Weekly":
        df_copy['Week'] = df_copy['Day'].dt.to_period('W').apply(lambda r: r.start_time)
        group_col = 'Week'
    elif tf == "Monthly":
        df_copy['Month'] = df_copy['Day'].dt.to_period('M').apply(lambda r: r.start_time)
        group_col = 'Month'
    elif tf == "Yearly":
        df_copy['Year'] = df_copy['Day'].dt.to_period('Y').apply(lambda r: r.start_time)
        group_col = 'Year'
    else:  # Default is 'Daily'
        group_col = 'Day'
    
    if tf == "Daily":
        cols = [group_col, col1] if not col2 else [group_col, col1, col2]
        return df_copy[cols].rename(columns={group_col: "Date"})

    agg = {col1: 'first'}
    if col2: 
        agg[col2] = 'mean' if capped else 'first'

    grouped = df_copy.groupby(group_col).agg(agg).reset_index()
    grouped.rename(columns={group_col: "Date"}, inplace=True)
    return grouped

# Create the plot for BTC vs LKR
def create_btc_plot(timeframe):
    data = prepare_data(timeframe, 'BTC vs LKR Interpolated')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['BTC vs LKR Interpolated'], name='BTC vs LKR', line=dict(color='red')))
    fig.update_layout(
        title=f"BTC vs LKR - {timeframe}",
        xaxis_title="Date",
        yaxis_title="BTC vs LKR",
        height=500
    )
    return fig

# Create the plot for USD vs LKR
def create_usd_plot(timeframe):
    data = prepare_data(timeframe, 'USD to LKR Price')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['USD to LKR Price'], name='USD vs LKR', line=dict(color='blue')))
    fig.update_layout(
        title=f"USD vs LKR - {timeframe}",
        xaxis_title="Date",
        yaxis_title="USD vs LKR",
        height=500
    )
    return fig

# Create dual-axis chart (BTC vs LKR & USD vs LKR)
def dual_axis_chart(timeframe):
    data_btc = prepare_data(timeframe, 'BTC vs LKR Interpolated')
    data_usd = prepare_data(timeframe, 'USD to LKR Price')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_btc['Date'], y=data_btc['BTC vs LKR Interpolated'], name='BTC vs LKR', line=dict(color='red'), yaxis='y1'))
    fig.add_trace(go.Scatter(x=data_usd['Date'], y=data_usd['USD to LKR Price'], name='USD to LKR', line=dict(color='Blue'), yaxis='y2'))
    
    fig.update_layout(
        title=f"BTC vs LKR & USD vs LKR - {timeframe}",
        xaxis_title="Date",
        yaxis=dict(title='BTC vs LKR', title_font=dict(color='White'), tickfont=dict(color='White')),
        yaxis2=dict(title='USD to LKR', title_font=dict(color='White'), tickfont=dict(color='White'), overlaying='y', side='right'),
        height=500,
        legend=dict(x=0.5, y=1.15, traceorder='normal', orientation='h', xanchor='center', yanchor='bottom'),
        margin=dict(l=50, r=50, t=80, b=50)  # Increased top margin to make space for legend above
    )
    
    return fig

# Create dual-axis chart for BTC vs Premium
def dual_axis_premium_chart(timeframe):
    data_btc = prepare_data(timeframe, 'BTC vs LKR Interpolated', 'Premium Capped', capped=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_btc['Date'], y=data_btc['BTC vs LKR Interpolated'], name='BTC vs LKR', line=dict(color='red'), yaxis='y1'))
    fig.add_trace(go.Scatter(x=data_btc['Date'], y=data_btc['Premium Capped'], name='P2P Premium (LKR)', line=dict(color='orange'), yaxis='y2'))
    
    fig.update_layout(
        title=f"BTC vs Premium - {timeframe}",
        xaxis_title="Date",
        yaxis=dict(title='BTC vs LKR', title_font=dict(color='White'), tickfont=dict(color='White')),
        yaxis2=dict(title='P2P Premium (LKR)', title_font=dict(color='White'), tickfont=dict(color='White'), overlaying='y', side='right'),
        height=500,
        legend=dict(x=0.5, y=1.15, traceorder='normal', orientation='h', xanchor='center', yanchor='bottom'),
        margin=dict(l=50, r=50, t=80, b=50)  # Increased top margin to make space for legend above
    )
    
    return fig

# Create dual-axis chart for USD vs Premium
def dual_axis_usd_premium_chart(timeframe):
    data_usd = prepare_data(timeframe, 'USD to LKR Price', 'Premium Capped', capped=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_usd['Date'], y=data_usd['USD to LKR Price'], name='USD to LKR', line=dict(color='blue'), yaxis='y1'))
    fig.add_trace(go.Scatter(x=data_usd['Date'], y=data_usd['Premium Capped'], name='P2P Premium (LKR)', line=dict(color='orange'), yaxis='y2'))
    
    fig.update_layout(
        title=f"USD vs Premium - {timeframe}",
        xaxis_title="Date",
        yaxis=dict(title='USD to LKR', title_font=dict(color='White'), tickfont=dict(color='White')),
        yaxis2=dict(title='P2P Premium (LKR)', title_font=dict(color='White'), tickfont=dict(color='White'), overlaying='y', side='right'),
        height=500,
        legend=dict(x=0.5, y=1.15, traceorder='normal', orientation='h', xanchor='center', yanchor='bottom'),
        margin=dict(l=50, r=50, t=80, b=50)  # Increased top margin to make space for legend above
    )
    
    return fig

# Streamlit App
st.title("P2P Market Data Analysis (2022 -2025)")


# Render BTC vs LKR plot based on selected timeframe for BTC
btc_timeframe = st.selectbox('Select Timeframe for BTC vs LKR:', ['Daily', 'Weekly', 'Monthly', 'Yearly'], index=0, key="btc_timeframe")
st.subheader(f"📊 BTC vs LKR ({btc_timeframe})")
st.plotly_chart(create_btc_plot(btc_timeframe), use_container_width=True)

# Render USD vs LKR plot based on selected timeframe for USD
usd_timeframe = st.selectbox('Select Timeframe for USD vs LKR:', ['Daily', 'Weekly', 'Monthly', 'Yearly'], index=0, key="usd_timeframe")
st.subheader(f"📊 USD vs LKR ({usd_timeframe})")
st.plotly_chart(create_usd_plot(usd_timeframe), use_container_width=True)

# Render dual-axis chart for BTC vs LKR & USD vs LKR based on selected timeframe
dual_axis_timeframe = st.selectbox('Select Timeframe for BTC vs LKR & USD vs LKR Dual-Axis:', ['Daily', 'Weekly', 'Monthly', 'Yearly'], index=0, key="dual_axis_timeframe")
st.subheader(f"📊 BTC vs LKR & USD vs LKR ({dual_axis_timeframe})")
st.plotly_chart(dual_axis_chart(dual_axis_timeframe), use_container_width=True)

# Render dual-axis chart for BTC vs Premium based on selected timeframe
btc_premium_timeframe = st.selectbox('Select Timeframe for BTC vs Premium:', ['Daily', 'Weekly', 'Monthly', 'Yearly'], index=0, key="btc_premium_timeframe")
st.subheader(f"📊 BTC vs Premium ({btc_premium_timeframe})")
st.plotly_chart(dual_axis_premium_chart(btc_premium_timeframe), use_container_width=True)

# Render dual-axis chart for USD vs Premium based on selected timeframe
usd_premium_timeframe = st.selectbox('Select Timeframe for USD vs Premium:', ['Daily', 'Weekly', 'Monthly', 'Yearly'], index=0, key="usd_premium_timeframe")
st.subheader(f"📊 USD vs Premium ({usd_premium_timeframe})")
st.plotly_chart(dual_axis_usd_premium_chart(usd_premium_timeframe), use_container_width=True)
