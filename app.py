# import streamlit as st

# # Sidebar for navigation
# st.sidebar.title("Dashboard Navigation")
# page = st.sidebar.radio("Select a Chart Type:", ["Merchant Activity", "P2P Buy Depth Chart", "P2P Market Data"])

# # Page navigation based on selected chart type
# if page == "Merchant Activity":
#     st.write("### Merchant Activity Dashboard")
#     st.write("This page will show the Merchant Activity Charts.")
# elif page == "P2P Buy Depth Chart":
#     st.write("### P2P Buy Depth Chart")
#     st.write("This page will show the P2P Buy Depth Chart.")
# elif page == "P2P Market Data":
#     st.write("### P2P Market Data")
#     st.write("This page will show the P2P Market Data Charts.")

import streamlit as st

# Sidebar for navigation
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio("Select a Chart Type:", [
    "Merchant Activity", 
    "P2P Buy Depth Chart", 
    "P2P Market Data", 
    "Merchant Volume", 
    "Merchant Leaderboard Count"
])

# Page navigation based on selected chart type
if page == "Merchant Activity":
    st.write("### Merchant Activity Dashboard")
    st.write("This page will show the Merchant Activity Charts.")
elif page == "P2P Buy Depth Chart":
    st.write("### P2P Buy Depth Chart")
    st.write("This page will show the P2P Buy Depth Chart.")
elif page == "P2P Market Data":
    st.write("### P2P Market Data")
    st.write("This page will show the P2P Market Data Charts.")
elif page == "Merchant Volume":
    st.write("### Merchant Volume Dashboard")
    st.write("This page will show Merchant Volume related charts.")
elif page == "Merchant Leaderboard Count":
    st.write("### Merchant Leaderboard Count")
    st.write("This page will show Merchant Leaderboard Count charts.")






