from datetime import datetime

def product_document(
    product_id, source, title, url,
    category, price, currency="GBP",
    rating=None, availability="In Stock",
    image_url=None, attributes=None
):
    now = datetime.utcnow()
    return {
        "product_id": product_id,
        "source": source,
        "title": title,
        "url": url,
        "category": category,
        "current_price": price,
        "currency": currency,
        "rating": rating,
        "availability": availability,
        "image_url": image_url,
        "attributes": attributes or {},
        "price_stats": {
            "all_time_low": price,
            "all_time_high": price,
            "avg_price": price,
            "last_checked": now
        },
        "created_at": now,
        "updated_at": now
    }

def price_history_document(product_id, price, source, currency="GBP", availability="In Stock", job_id=None):
    return {
        "product_id": product_id,
        "price": price,
        "currency": currency,
        "availability": availability,
        "scraped_at": datetime.utcnow(),
        "source": source,
        "scrape_job_id": job_id
    }

def alert_document(product_id, price_before, price_after, threshold_pct):
    drop_pct = round(((price_before - price_after) / price_before) * 100, 2)
    return {
        "product_id": product_id,
        "alert_type": "price_drop",
        "threshold_pct": threshold_pct,
        "price_before": price_before,
        "price_after": price_after,
        "drop_percentage": drop_pct,
        "triggered_at": datetime.utcnow(),
        "notified": False,
        "notification_channel": "email"
    }

def scrape_log_document(job_id, source):
    return {
        "job_id": job_id,
        "source": source,
        "started_at": datetime.utcnow(),
        "completed_at": None,
        "products_scraped": 0,
        "new_products": 0,
        "price_changes": 0,
        "errors": [],
        "status": "running"
    }