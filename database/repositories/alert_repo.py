from datetime import datetime
from database.connection import get_db

def insert_alert(product_id, price_before, price_after, drop_pct):
    db = get_db()
    doc = {
        "product_id": product_id,
        "alert_type": "price_drop",
        "threshold_pct": float(os.getenv("PRICE_DROP_THRESHOLD", 10)),
        "price_before": price_before,
        "price_after": price_after,
        "drop_percentage": drop_pct,
        "triggered_at": datetime.utcnow(),
        "notified": False,
        "notification_channel": "email"
    }
    db.alerts.insert_one(doc)
    return doc

def get_recent_alerts(limit=20):
    db = get_db()
    return list(db.alerts.find(
        {},
        {"_id": 0}
    ).sort("triggered_at", -1).limit(limit))

def setup_indexes():
    db = get_db()
    db.alerts.create_index([("product_id", 1), ("triggered_at", -1)])
    print("✅ Alert indexes created")