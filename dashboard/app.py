import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dashboard.pages import overview, catalog, trends, deals

st.set_page_config(
    page_title="Price Tracker",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🛒 Price Tracker")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Overview", "📦 Catalog", "📈 Trends", "🔥 Deals"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Python + MongoDB")

if page == "📊 Overview":
    overview.show()
elif page == "📦 Catalog":
    catalog.show()
elif page == "📈 Trends":
    trends.show()
elif page == "🔥 Deals":
    deals.show()