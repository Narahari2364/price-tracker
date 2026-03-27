from datetime import datetime
from database.connection import get_db

def upsert_product(product: dict) -> dict:
    db = get_db()
    now = datetime.utcnow()
    existing = db.products.find_one({"product_id": product["product_id"]})

    if existing:
        old_price = existing["current_price"]
        new_price = product["current_price"]
        stats = existing.get("price_stats", {})

        updated_stats = {
            "all_time_low": min(stats.get("all_time_low", old_price), new_price),
            "all_time_high": max(stats.get("all_time_high", old_price), new_price),
            "avg_price": round((stats.get("avg_price", old_price) + new_price) / 2, 2),
            "last_checked": now
        }

        db.products.update_one(
            {"product_id": product["product_id"]},
            {"$set": {
                "current_price": new_price,
                "availability": product["availability"],
                "price_stats": updated_stats,
                "updated_at": now
            }}
        )
        return {"status": "updated", "product_id": product["product_id"], "old_price": old_price, "new_price": new_price}
    else:
        doc = {**product,
               "price_stats": {
                   "all_time_low": product["current_price"],
                   "all_time_high": product["current_price"],
                   "avg_price": product["current_price"],
                   "last_checked": now
               },
               "created_at": now,
               "updated_at": now
        }
        db.products.insert_one(doc)
        return {"status": "inserted", "product_id": product["product_id"]}

def get_all_products(filters=None):
    db = get_db()
    return list(db.products.find(filters or {}, {"_id": 0}))

def get_product_by_id(product_id: str):
    db = get_db()
    return db.products.find_one({"product_id": product_id}, {"_id": 0})

def setup_indexes():
    db = get_db()
    db.products.create_index("product_id", unique=True)
    db.products.create_index("category")
    db.products.create_index("current_price")
    print("✅ Product indexes created")