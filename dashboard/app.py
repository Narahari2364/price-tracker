import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dashboard.views import overview, catalog, trends, deals

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

st.markdown("""
    <div style="
        background: linear-gradient(90deg, #667eea, #764ba2);
        padding: 1.5rem 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1.5rem;
    ">
        <h1 style="
            font-size: 2.4rem;
            font-weight: 800;
            margin: 0 0 0.25rem 0;
        ">
            🛒 Price Tracker
        </h1>
        <p style="
            font-size: 0.95rem;
            margin: 0;
            opacity: 0.9;
        ">
            Automated e-commerce price monitoring · 1,020 products · 30,600+ price records
        </p>
    </div>
""", unsafe_allow_html=True)

if page == "📊 Overview":
    overview.show()
elif page == "📦 Catalog":
    catalog.show()
elif page == "📈 Trends":
    trends.show()
elif page == "🔥 Deals":
    deals.show()