import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.books_scraper import BooksScraper
from scrapers.fakestore_scraper import FakeStoreScraper
from database.repositories.product_repo import upsert_product, setup_indexes
from database.repositories.price_repo import insert_price_snapshot, setup_indexes as price_indexes
from database.connection import test_connection

def seed():
    print("🌱 Starting data seed...\\n")

    if not test_connection():
        print("❌ Cannot connect to MongoDB. Exiting.")
        return

    print("\\n📦 Setting up indexes...")
    setup_indexes()
    price_indexes()

    # Scrape books
    print("\\n📚 Scraping books...")
    books_scraper = BooksScraper()
    books = books_scraper.scrape()

    inserted = updated = 0
    for book in books:
        result = upsert_product(book)
        insert_price_snapshot(
            product_id=book["product_id"],
            price=book["current_price"],
            source=book["source"],
            currency=book["currency"],
            availability=book["availability"],
            job_id="seed_001"
        )
        if result["status"] == "inserted":
            inserted += 1
        else:
            updated += 1

    print(f"  ✅ Books — Inserted: {inserted} | Updated: {updated}")

    # Scrape fake store
    print("\\n🛍️  Scraping Fake Store products...")
    fakestore_scraper = FakeStoreScraper()
    products = fakestore_scraper.scrape()

    inserted = updated = 0
    for product in products:
        result = upsert_product(product)
        insert_price_snapshot(
            product_id=product["product_id"],
            price=product["current_price"],
            source=product["source"],
            currency=product["currency"],
            availability=product["availability"],
            job_id="seed_001"
        )
        if result["status"] == "inserted":
            inserted += 1
        else:
            updated += 1

    print(f"  ✅ Fake Store — Inserted: {inserted} | Updated: {updated}")
    print("\\n🎉 Seed complete! Check your MongoDB Atlas collections.")

if __name__ == "__main__":
    seed()