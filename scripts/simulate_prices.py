import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from datetime import datetime, timedelta
from database.connection import get_db, test_connection
from database.repositories.alert_repo import setup_indexes

print("🚀 Script started!", flush=True)

def simulate_price_history(days=30):
    print("📈 Simulating 30 days of price history...", flush=True)

    if not test_connection():
        print("❌ Cannot connect to MongoDB. Exiting.", flush=True)
        return

    setup_indexes()
    db = get_db()

    products = list(db.products.find({}, {"product_id": 1, "current_price": 1, "source": 1, "currency": 1}))
    print(f"  Found {len(products)} products to simulate", flush=True)

    db.price_history.delete_many({"scrape_job_id": {"$regex": "^sim_"}})
    print("  🗑️  Cleared old simulation data", flush=True)

    total_inserted = 0
    base_date = datetime.utcnow() - timedelta(days=days)

    for i, product in enumerate(products):
        pid = product["product_id"]
        base_price = product["current_price"]
        currency = product.get("currency", "GBP")
        source = product.get("source", "unknown")

        price = base_price
        snapshots = []

        for day in range(days):
            date = base_date + timedelta(days=day)
            change_pct = random.uniform(-0.05, 0.05)
            if random.random() < 0.05:
                change_pct = random.uniform(-0.20, -0.10)
            price = round(max(0.99, price * (1 + change_pct)), 2)
            job_id = f"sim_{date.strftime('%Y%m%d')}"
            snapshots.append({
                "product_id": pid,
                "price": price,
                "currency": currency,
                "availability": "In Stock",
                "scraped_at": date,
                "source": source,
                "scrape_job_id": job_id
            })

        db.price_history.insert_many(snapshots)
        total_inserted += len(snapshots)

        if (i + 1) % 100 == 0:
            print(f"  ✅ Simulated {i + 1}/{len(products)} products...", flush=True)

    print(f"\\n🎉 Simulation complete!", flush=True)
    print(f"   Total price history records: {total_inserted}", flush=True)
    print(f"   That's {days} days × {len(products)} products", flush=True)

simulate_price_history(days=30)