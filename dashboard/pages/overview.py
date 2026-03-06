import streamlit as st
from database.connection import get_db
from dashboard.components.charts import category_bar_chart, price_distribution_chart

def show():
    st.title("📊 Overview")
    db = get_db()

    total_products = db.products.count_documents({})
    total_history = db.price_history.count_documents({})
    total_alerts = db.alerts.count_documents({})
    recent_alerts = db.alerts.count_documents({"notified": False})

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🛍️ Total Products", f"{total_products:,}")
    col2.metric("📈 Price Records", f"{total_history:,}")
    col3.metric("🔔 Total Alerts", f"{total_alerts:,}")
    col4.metric("🆕 Unread Alerts", f"{recent_alerts:,}")

    st.divider()

    products = list(db.products.find({}, {"_id": 0}))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(category_bar_chart(products), use_container_width=True)
    with col2:
        st.plotly_chart(price_distribution_chart(products), use_container_width=True)

    st.divider()
    st.subheader("🕐 Recently Updated Products")
    recent = list(db.products.find(
        {}, {"_id": 0, "title": 1, "current_price": 1, "currency": 1, "category": 1, "source": 1}
    ).sort("updated_at", -1).limit(10))

    if recent:
        import pandas as pd
        df = pd.DataFrame(recent)
        st.dataframe(df, use_container_width=True)