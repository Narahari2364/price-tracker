import requests
from scrapers.base_scraper import BaseScraper
from scrapers.middleware.rate_limiter import short_delay

BASE_URL = "https://fakestoreapi.com"

CATEGORY_MAP = {
    "electronics": "Electronics",
    "jewelery": "Jewellery",
    "men's clothing": "Clothing",
    "women's clothing": "Clothing"
}

class FakeStoreScraper(BaseScraper):
    def __init__(self):
        super().__init__(BASE_URL, "fakestoreapi.com")

    def scrape(self):
        products = []
        print(f"🕷️  Starting scrape of {self.source_name}...")
        try:
            response = requests.get(f"{BASE_URL}/products", timeout=15)
            response.raise_for_status()
            items = response.json()
            for item in items:
                product = self.parse_product(item)
                if product:
                    products.append(product)
                short_delay()
            print(f"🎉 Scraping complete! Total products: {len(products)}")
        except Exception as e:
            print(f"❌ Error scraping Fake Store: {e}")
        return products

    def parse_product(self, item):
        try:
            category = CATEGORY_MAP.get(item.get("category", ""), "General")
            return {
                "product_id": f"fakestore_{item['id']}",
                "source": self.source_name,
                "title": item["title"],
                "url": f"{BASE_URL}/products/{item['id']}",
                "category": category,
                "current_price": float(item["price"]),
                "currency": "USD",
                "rating": float(item["rating"]["rate"]),
                "availability": "In Stock",
                "image_url": item["image"],
                "attributes": {
                    "description": item.get("description", ""),
                    "rating_count": item["rating"]["count"]
                }
            }
        except Exception as e:
            print(f"  ⚠️ Failed to parse product: {e}")
            return None

if __name__ == "__main__":
    scraper = FakeStoreScraper()
    products = scraper.scrape()
    print(f"\\nSample product: {products[0]}")