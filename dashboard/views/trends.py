import streamlit as st
from database.connection import get_db
from dashboard.components.charts import price_trend_chart

def show():
    st.title("📈 Price Trends")
    db = get_db()

    products = list(db.products.find(
        {}, {"_id": 0, "product_id": 1, "title": 1, "current_price": 1, "currency": 1}
    ).limit(200))

    if not products:
        st.warning("No products found.")
        return

    options = {p["title"][:60]: p["product_id"] for p in products}
    selected_title = st.selectbox("🔍 Select a product", list(options.keys()))
    selected_id = options[selected_title]

    history = list(db.price_history.find(
        {"product_id": selected_id},
        {"_id": 0}
    ).sort("scraped_at", 1))

    if not history:
        st.warning("No price history found for this product.")
        return

    product = db.products.find_one({"product_id": selected_id}, {"_id": 0})
    currency = product.get("currency", "")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Current Price", f"{currency} {product['current_price']}")
    col2.metric("📉 All Time Low", f"{currency} {product['price_stats']['all_time_low']}")
    col3.metric("📈 All Time High", f"{currency} {product['price_stats']['all_time_high']}")

    st.plotly_chart(
        price_trend_chart(history, f"Price History: {selected_title[:50]}"),
        use_container_width=True
    )

    st.subheader("📋 Raw Price History")
    import pandas as pd
    df = pd.DataFrame(history)[["scraped_at", "price", "currency", "availability"]]
    df.columns = ["Date", "Price", "Currency", "Availability"]
    st.dataframe(df, use_container_width=True)