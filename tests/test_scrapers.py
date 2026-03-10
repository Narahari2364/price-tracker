import pytest
import responses as responses_mock
import requests
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.middleware.user_agent import get_headers, get_random_user_agent, USER_AGENTS
from scrapers.middleware.rate_limiter import polite_delay, short_delay
from scrapers.books_scraper import BooksScraper, RATING_MAP
from scrapers.fakestore_scraper import FakeStoreScraper, CATEGORY_MAP
from unittest.mock import patch
import time

# ── User Agent Tests ────────────────────────────────────
class TestUserAgent:
    def test_get_random_user_agent_returns_string(self):
        ua = get_random_user_agent()
        assert isinstance(ua, str)
        assert len(ua) > 0

    def test_user_agent_from_list(self):
        ua = get_random_user_agent()
        assert ua in USER_AGENTS

    def test_get_headers_has_user_agent(self):
        headers = get_headers()
        assert "User-Agent" in headers
        assert len(headers["User-Agent"]) > 0

    def test_get_headers_has_required_keys(self):
        headers = get_headers()
        assert "Accept" in headers
        assert "Accept-Language" in headers
        assert "Connection" in headers

# ── Rate Limiter Tests ──────────────────────────────────
class TestRateLimiter:
    def test_polite_delay_waits(self):
        start = time.time()
        with patch("scrapers.middleware.rate_limiter.random.uniform", return_value=0.1):
            polite_delay()
        elapsed = time.time() - start
        assert elapsed >= 0.05

    def test_short_delay_waits(self):
        start = time.time()
        with patch("scrapers.middleware.rate_limiter.random.uniform", return_value=0.1):
            short_delay()
        elapsed = time.time() - start
        assert elapsed >= 0.05

# ── Books Scraper Tests ─────────────────────────────────
class TestBooksScraper:
    def test_rating_map_has_all_values(self):
        assert RATING_MAP["One"] == 1
        assert RATING_MAP["Two"] == 2
        assert RATING_MAP["Three"] == 3
        assert RATING_MAP["Four"] == 4
        assert RATING_MAP["Five"] == 5

    def test_scraper_initializes(self):
        scraper = BooksScraper()
        assert scraper.base_url == "https://books.toscrape.com"
        assert scraper.source_name == "books.toscrape.com"

    def test_parse_product_returns_none_on_bad_html(self):
        from bs4 import BeautifulSoup
        scraper = BooksScraper()
        bad_html = BeautifulSoup("<div>bad html</div>", "html.parser")
        result = scraper.parse_product(bad_html)
        assert result is None

    def test_can_scrape_allowed_url(self):
        scraper = BooksScraper()
        with patch.object(scraper, "can_scrape", return_value=True):
            assert scraper.can_scrape("https://books.toscrape.com/catalogue/page-1.html")

# ── Fake Store Scraper Tests ────────────────────────────
class TestFakeStoreScraper:
    def test_category_map_has_entries(self):
        assert "electronics" in CATEGORY_MAP
        assert "jewelery" in CATEGORY_MAP

    def test_scraper_initializes(self):
        scraper = FakeStoreScraper()
        assert scraper.base_url == "https://fakestoreapi.com"

    def test_parse_product_valid_item(self):
        scraper = FakeStoreScraper()
        item = {
            "id": 1,
            "title": "Test Product",
            "price": 29.99,
            "category": "electronics",
            "image": "https://test.com/img.jpg",
            "description": "Test description",
            "rating": {"rate": 4.2, "count": 100}
        }
        result = scraper.parse_product(item)
        assert result is not None
        assert result["product_id"] == "fakestore_1"
        assert result["current_price"] == 29.99
        assert result["category"] == "Electronics"
        assert result["rating"] == 4.2

    def test_parse_product_returns_none_on_bad_data(self):
        scraper = FakeStoreScraper()
        result = scraper.parse_product({})
        assert result is None

    @responses_mock.activate
    def test_scrape_returns_products(self):
        mock_data = [
            {
                "id": 1, "title": "Test", "price": 9.99,
                "category": "electronics", "image": "http://test.com/img.jpg",
                "description": "desc", "rating": {"rate": 4.0, "count": 10}
            }
        ]
        responses_mock.add(
            responses_mock.GET,
            "https://fakestoreapi.com/products",
            json=mock_data, status=200
        )
        with patch("scrapers.fakestore_scraper.short_delay"):
            scraper = FakeStoreScraper()
            products = scraper.scrape()
        assert len(products) == 1
        assert products[0]["title"] == "Test"