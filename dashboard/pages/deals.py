import streamlit as st
import pandas as pd
from database.connection import get_db

def show():
    st.title("🔥 Deals & Alerts")
    db = get_db()

    alerts = list(db.alerts.find({}, {"_id": 0}).sort("triggered_at", -1).limit(50))

    if not alerts:
        st.info("No alerts yet. Run the scraper a few times to generate price drop alerts!")
        st.markdown("---")

    st.subheader("💸 Best Current Deals")
    deals = list(db.products.find(
        {},
        {"_id": 0, "title": 1, "current_price": 1, "currency": 1,
         "category": 1, "price_stats": 1, "source": 1}
    ).sort("current_price", 1).limit(20))

    if deals:
        rows = []
        for d in deals:
            stats = d.get("price_stats", {})
            high = stats.get("all_time_high", d["current_price"])
            low = stats.get("all_time_low", d["current_price"])
            saving = round(high - d["current_price"], 2)
            rows.append({
                "Title": d["title"][:50],
                "Current Price": f"{d['currency']} {d['current_price']}",
                "All Time High": f"{d['currency']} {high}",
                "All Time Low": f"{d['currency']} {low}",
                "Saving vs High": f"{d['currency']} {saving}",
                "Category": d["category"],
                "Source": d["source"]
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    if alerts:
        st.divider()
        st.subheader("🔔 Recent Price Drop Alerts")
        df = pd.DataFrame(alerts)[[
            "product_id", "price_before", "price_after", "drop_percentage", "triggered_at"
        ]]
        df.columns = ["Product ID", "Price Before", "Price After", "Drop %", "Triggered At"]
        st.dataframe(df, use_container_width=True)