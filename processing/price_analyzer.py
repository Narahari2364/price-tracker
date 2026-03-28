import os
from dotenv import load_dotenv
from database.connection import get_db

load_dotenv()

THRESHOLD = float(os.getenv("PRICE_DROP_THRESHOLD", 10))

def get_previous_price(product_id: str, current_job_id: str):
    db = get_db()
    record = db.price_history.find_one(
        {"product_id": product_id, "scrape_job_id": {"$ne": current_job_id}},
        sort=[("scraped_at", -1)]
    )
    return record["price"] if record else None

def calculate_drop_pct(old_price, new_price):
    if not old_price or old_price == 0:
        return 0
    return round(((old_price - new_price) / old_price) * 100, 2)

def analyze_price_changes(job_id: str):
    db = get_db()
    products = list(db.products.find({}, {"_id": 0}))
    drops = []

    print(f"🔍 Analyzing price changes for {len(products)} products...")

    for p in products:
        pid = p["product_id"]
        current_price = p["current_price"]
        prev_price = get_previous_price(pid, job_id)

        if prev_price is None:
            continue

        drop_pct = calculate_drop_pct(prev_price, current_price)

        if drop_pct >= THRESHOLD:
            drops.append({
                "product_id": pid,
                "title": p["title"],
                "price_before": prev_price,
                "price_after": current_price,
                "drop_pct": drop_pct,
                "currency": p["currency"]
            })

    print(f"  ✅ Found {len(drops)} price drops above {THRESHOLD}%")
    return drops