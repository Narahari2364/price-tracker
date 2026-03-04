from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from scrapers.middleware.retry import fetch_page
from scrapers.middleware.rate_limiter import polite_delay

BASE_URL = "https://books.toscrape.com"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

class BooksScraper(BaseScraper):
    def __init__(self):
        super().__init__(BASE_URL, "books.toscrape.com")

    def scrape(self):
        products = []
        page = 1
        print(f"🕷️  Starting scrape of {self.source_name}...")

        while True:
            url = f"{BASE_URL}/catalogue/page-{page}.html"
            if not self.can_scrape(url):
                print(f"⛔ robots.txt disallows scraping: {url}")
                break

            try:
                response = fetch_page(url)
                soup = BeautifulSoup(response.text, "html.parser")
                books = soup.select("article.product_pod")

                if not books:
                    break

                for book in books:
                    product = self.parse_product(book)
                    if product:
                        products.append(product)

                print(f"  ✅ Page {page} scraped — {len(products)} books so far")
                page += 1
                polite_delay()

            except Exception as e:
                print(f"  ❌ Error on page {page}: {e}")
                break

        print(f"🎉 Scraping complete! Total books: {len(products)}")
        return products

    def parse_product(self, book_html):
        try:
            title = book_html.select_one("h3 a")["title"]
            relative_url = book_html.select_one("h3 a")["href"].replace("../", "")
            url = f"{BASE_URL}/catalogue/{relative_url}"
            price_text = book_html.select_one("p.price_color").text.strip()
            price = float(price_text.replace("£", "").replace("Â", "").strip())
            rating_class = book_html.select_one("p.star-rating")["class"][1]
            rating = RATING_MAP.get(rating_class, 0)
            availability = book_html.select_one("p.availability").text.strip()
            category = "Books"
            product_id = f"book_{url.split('/')[-2]}"
            image_path = book_html.select_one("img.thumbnail")["src"].replace("../", "")
            image_url = f"{BASE_URL}/{image_path}"

            return {
                "product_id": product_id,
                "source": self.source_name,
                "title": title,
                "url": url,
                "category": category,
                "current_price": price,
                "currency": "GBP",
                "rating": rating,
                "availability": availability,
                "image_url": image_url,
                "attributes": {}
            }
        except Exception as e:
            print(f"    ⚠️ Failed to parse book: {e}")
            return None


if __name__ == "__main__":
    scraper = BooksScraper()
    books = scraper.scrape()
    print(f"\nSample book: {books[0]}")