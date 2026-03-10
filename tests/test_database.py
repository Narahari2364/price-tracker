import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock, patch
from datetime import datetime

# ── Product Repo Tests ──────────────────────────────────
class TestProductRepo:
    def test_upsert_inserts_new_product(self, sample_book):
        mock_db = MagicMock()
        mock_db.products.find_one.return_value = None

        with patch("database.repositories.product_repo.get_db", return_value=mock_db):
            from database.repositories.product_repo import upsert_product
            result = upsert_product(sample_book)

        assert result["status"] == "inserted"
        mock_db.products.insert_one.assert_called_once()

    def test_upsert_updates_existing_product(self, sample_book):
        mock_db = MagicMock()
        mock_db.products.find_one.return_value = {
            **sample_book,
            "price_stats": {
                "all_time_low": 12.99,
                "all_time_high": 16.99,
                "avg_price": 14.99
            }
        }

        with patch("database.repositories.product_repo.get_db", return_value=mock_db):
            from database.repositories.product_repo import upsert_product
            result = upsert_product(sample_book)

        assert result["status"] == "updated"
        mock_db.products.update_one.assert_called_once()

    def test_get_product_by_id(self, sample_book):
        mock_db = MagicMock()
        mock_db.products.find_one.return_value = sample_book

        with patch("database.repositories.product_repo.get_db", return_value=mock_db):
            from database.repositories.product_repo import get_product_by_id
            result = get_product_by_id("book_test_123")

        assert result["product_id"] == "book_test_123"

# ── Price Repo Tests ────────────────────────────────────
class TestPriceRepo:
    def test_insert_price_snapshot(self):
        mock_db = MagicMock()

        with patch("database.repositories.price_repo.get_db", return_value=mock_db):
            from database.repositories.price_repo import insert_price_snapshot
            result = insert_price_snapshot(
                product_id="book_test_123",
                price=14.99,
                source="books.toscrape.com",
                currency="GBP",
                job_id="test_job"
            )

        assert result["product_id"] == "book_test_123"
        assert result["price"] == 14.99
        mock_db.price_history.insert_one.assert_called_once()

    def test_get_price_history(self, sample_price_history):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.sort.return_value.limit.return_value = sample_price_history
        mock_db.price_history.find.return_value = mock_cursor

        with patch("database.repositories.price_repo.get_db", return_value=mock_db):
            from database.repositories.price_repo import get_price_history
            result = get_price_history("book_test_123")

        assert len(result) == 3

# ── Alert Repo Tests ────────────────────────────────────
class TestAlertRepo:
    def test_insert_alert(self, sample_alert):
        mock_db = MagicMock()
        mock_db.alerts.insert_one.return_value = MagicMock(inserted_id="test_id")

        with patch("database.repositories.alert_repo.get_db", return_value=mock_db):
            with patch("database.repositories.alert_repo.os.getenv", return_value="10"):
                from database.repositories import alert_repo
                import importlib
                importlib.reload(alert_repo)
                alert_repo.get_db = lambda: mock_db
                alert_repo.insert_alert(
                    product_id="book_test_123",
                    price_before=14.99,
                    price_after=10.99,
                    drop_pct=26.68
                )
                mock_db.alerts.insert_one.assert_called_once()