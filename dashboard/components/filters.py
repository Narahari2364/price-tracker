import streamlit as st

def category_filter(products: list):
    categories = sorted(set(p["category"] for p in products))
    return st.sidebar.multiselect(
        "📂 Category",
        options=categories,
        default=categories
    )

def price_filter(products: list):
    if not products:
        return 0.0, 1000.0
    prices = [p["current_price"] for p in products]
    min_p, max_p = min(prices), max(prices)
    return st.sidebar.slider(
        "💰 Price Range",
        min_value=float(min_p),
        max_value=float(max_p),
        value=(float(min_p), float(max_p))
    )

def rating_filter():
    return st.sidebar.slider(
        "⭐ Minimum Rating",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.5
    )

def source_filter(products: list):
    sources = sorted(set(p["source"] for p in products))
    return st.sidebar.multiselect(
        "🌐 Source",
        options=sources,
        default=sources
    )

def apply_filters(products, categories, price_range, min_rating, sources):
    return [
        p for p in products
        if p["category"] in categories
        and price_range[0] <= p["current_price"] <= price_range[1]
        and (p.get("rating") or 0) >= min_rating
        and p["source"] in sources
    ]