import streamlit as st
import pandas as pd
from database.connection import get_db
from dashboard.components.filters import (
    category_filter, price_filter, rating_filter, source_filter, apply_filters
)

def show():
    st.title("📦 Product Catalog")
    db = get_db()
    products = list(db.products.find({}, {"_id": 0}))

    if not products:
        st.warning("No products found.")
        return

    st.sidebar.header("🔍 Filters")
    categories = category_filter(products)
    price_range = price_filter(products)
    min_rating = rating_filter()
    sources = source_filter(products)

    filtered = apply_filters(products, categories, price_range, min_rating, sources)

    st.markdown(f"Showing **{len(filtered)}** of **{len(products)}** products")
    search = st.text_input("🔎 Search by title", "")
    if search:
        filtered = [p for p in filtered if search.lower() in p["title"].lower()]

    if filtered:
        df = pd.DataFrame(filtered)[
            ["title", "current_price", "currency", "category", "rating", "availability", "source"]
        ]
        df.columns = ["Title", "Price", "Currency", "Category", "Rating", "Availability", "Source"]
        st.dataframe(df, use_container_width=True, height=500)
    else:
        st.info("No products match your filters.")