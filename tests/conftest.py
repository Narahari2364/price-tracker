import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock, patch
from datetime import datetime

@pytest.fixture
def sample_book():
    return {
        "product_id": "book_test_123",
        "source": "books.toscrape.com",
        "title": "Test Book Title",
        "url": "https://books.toscrape.com/catalogue/test_123/index.html",
        "category": "Books",
        "current_price": 14.99,
        "currency": "GBP",
        "rating": 4,
        "availability": "In Stock",
        "image_url": "https://books.toscrape.com/media/test.jpg",
        "attributes": {}
    }

@pytest.fixture
def sample_product():
    return {
        "product_id": "fakestore_1",
        "source": "fakestoreapi.com",
        "title": "Test Electronics Product",
        "url": "https://fakestoreapi.com/products/1",
        "category": "Electronics",
        "current_price": 109.95,
        "currency": "USD",
        "rating": 3.9,
        "availability": "In Stock",
        "image_url": "https://fakestoreapi.com/img/test.png",
        "attributes": {"description": "Test description", "rating_count": 120}
    }

@pytest.fixture
def sample_price_history():
    return [
        {
            "product_id": "book_test_123",
            "price": 14.99,
            "scraped_at": datetime(2026, 1, 1),
            "scrape_job_id": "job_1",
        },
        {
            "product_id": "book_test_123",
            "price": 12.99,
            "scraped_at": datetime(2026, 1, 2),
            "scrape_job_id": "job_2",
        },
        {
            "product_id": "book_test_123",
            "price": 10.99,
            "scraped_at": datetime(2026, 1, 3),
            "scrape_job_id": "job_3",
        },
    ]


@pytest.fixture
def sample_alert():
    return {
        "product_id": "book_test_123",
        "alert_type": "price_drop",
        "threshold_pct": 10.0,
        "price_before": 14.99,
        "price_after": 10.99,
        "drop_percentage": 26.68,
        "notified": False,
        "notification_channel": "email",
    }