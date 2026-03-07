import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from scrapers.books_scraper import BooksScraper
from scrapers.fakestore_scraper import FakeStoreScraper
from database.repositories.product_repo import upsert_product
from database.repositories.price_repo import insert_price_snapshot
from processing.alert_engine import run_alert_engine
from alerts.email_alert import send_bulk_alerts

def run_scrape_job():
    job_id = f"job_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    print(f"\\n🚀 Starting scrape job: {job_id}")

    all_products = []

    # Scrape books
    try:
        books_scraper = BooksScraper()
        books = books_scraper.scrape()
        all_products.extend(books)
    except Exception as e:
        print(f"❌ Books scraper failed: {e}")

    # Scrape fake store
    try:
        fakestore_scraper = FakeStoreScraper()
        products = fakestore_scraper.scrape()
        all_products.extend(products)
    except Exception as e:
        print(f"❌ Fake Store scraper failed: {e}")

    # Save to MongoDB
    inserted = updated = 0
    for product in all_products:
        result = upsert_product(product)
        insert_price_snapshot(
            product_id=product["product_id"],
            price=product["current_price"],
            source=product["source"],
            currency=product["currency"],
            availability=product["availability"],
            job_id=job_id
        )
        if result["status"] == "inserted":
            inserted += 1
        else:
            updated += 1

    print(f"✅ Saved — Inserted: {inserted} | Updated: {updated}")

    # Run alerts
    alerts = run_alert_engine(job_id)

    # Send emails
    if alerts:
        sent = send_bulk_alerts(alerts)
        print(f"📧 Emails sent: {sent}")

    print(f"✅ Job {job_id} complete!\\n")