import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_db
from datetime import datetime
from processing.alert_engine import run_alert_engine
from alerts.email_alert import send_bulk_alerts

db = get_db()

# Get a product
product = db.products.find_one({"source": "books.toscrape.com"})
pid = product["product_id"]
old_price = product["current_price"]
new_price = round(old_price * 0.50, 2)

# Insert old price as yesterday
db.price_history.insert_one({
    "product_id": pid,
    "price": old_price,
    "currency": "GBP",
    "availability": "In Stock",
    "scraped_at": datetime.utcnow(),
    "source": "books.toscrape.com",
    "scrape_job_id": "test_yesterday"
})

# Force new lower price
db.products.update_one(
    {"product_id": pid},
    {"$set": {"current_price": new_price}}
)

# Insert new low price
db.price_history.insert_one({
    "product_id": pid,
    "price": new_price,
    "currency": "GBP",
    "availability": "In Stock",
    "scraped_at": datetime.utcnow(),
    "source": "books.toscrape.com",
    "scrape_job_id": "test_today"
})

print(f"✅ Forced price drop: {old_price} -> {new_price} for {product['title']}")

# Run alert engine
alerts = run_alert_engine("test_today")
if alerts:
    sent = send_bulk_alerts(alerts)
    print(f"📧 Emails sent: {sent}")
else:
    print("⚠️ No alerts generated")