import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processing.cleaner import clean_price, clean_product, clean_products
from processing.price_analyzer import calculate_drop_pct

# ── Cleaner Tests ───────────────────────────────────────
class TestCleaner:
    def test_clean_price_float(self):
        assert clean_price(14.99) == 14.99

    def test_clean_price_string_with_symbol(self):
        assert clean_price("£14.99") == 14.99

    def test_clean_price_string_with_dollar(self):
        assert clean_price("$109.95") == 109.95

    def test_clean_price_invalid_returns_none(self):
        assert clean_price("not a price") is None

    def test_clean_price_integer(self):
        assert clean_price(10) == 10.0

    def test_clean_product_strips_title(self):
        product = {"title": "  Test Book  ", "current_price": 14.99}
        result = clean_product(product)
        assert result["title"] == "Test Book"

    def test_clean_product_fixes_price(self):
        product = {"title": "Test", "current_price": "£14.99"}
        result = clean_product(product)
        assert result["current_price"] == 14.99

    def test_clean_product_fixes_rating(self):
        product = {"title": "Test", "current_price": 14.99, "rating": "4.5"}
        result = clean_product(product)
        assert result["rating"] == 4.5

    def test_clean_products_removes_invalid(self):
        products = [
            {"title": "Valid", "current_price": 9.99},
            {"title": "", "current_price": None},
            {"title": "Also Valid", "current_price": 5.99}
        ]
        result = clean_products(products)
        assert len(result) == 2

    def test_clean_products_empty_list(self):
        assert clean_products([]) == []

# ── Price Analyzer Tests ────────────────────────────────
class TestPriceAnalyzer:
    def test_calculate_drop_pct_basic(self):
        result = calculate_drop_pct(100.0, 80.0)
        assert result == 20.0

    def test_calculate_drop_pct_no_drop(self):
        result = calculate_drop_pct(100.0, 100.0)
        assert result == 0.0

    def test_calculate_drop_pct_price_increase(self):
        result = calculate_drop_pct(80.0, 100.0)
        assert result < 0

    def test_calculate_drop_pct_zero_old_price(self):
        result = calculate_drop_pct(0, 10.0)
        assert result == 0

    def test_calculate_drop_pct_rounds_correctly(self):
        result = calculate_drop_pct(14.99, 10.99)
        assert isinstance(result, float)
        assert result > 0