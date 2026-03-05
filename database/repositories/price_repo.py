from datetime import datetime
from database.connection import get_db

def insert_price_snapshot(product_id: str, price: float, source: str,
                           currency="GBP", availability="In Stock", job_id=None):
    db = get_db()
    doc = {
        "product_id": product_id,
        "price": price,
        "currency": currency,
        "availability": availability,
        "scraped_at": datetime.utcnow(),
        "source": source,
        "scrape_job_id": job_id
    }
    db.price_history.insert_one(doc)
    return doc

def get_price_history(product_id: str, limit=30):
    db = get_db()
    return list(db.price_history.find(
        {"product_id": product_id},
        {"_id": 0}
    ).sort("scraped_at", -1).limit(limit))

def setup_indexes():
    db = get_db()
    db.price_history.create_index([("product_id", 1), ("scraped_at", -1)])
    print("✅ Price history indexes created")