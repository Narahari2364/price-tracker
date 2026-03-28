import re

def clean_price(price_str):
    if isinstance(price_str, (int, float)):
        return round(float(price_str), 2)
    cleaned = re.sub(
        r"[^\d.]",
        "",
        str(price_str).encode("ascii", "ignore").decode(),
    )
    try:
        return round(float(cleaned), 2)
    except ValueError:
        return None

def clean_product(product: dict) -> dict:
    if product.get("current_price"):
        product["current_price"] = clean_price(product["current_price"])
    if product.get("title"):
        product["title"] = product["title"].strip()
    if product.get("availability"):
        product["availability"] = product["availability"].strip()
    if product.get("rating"):
        try:
            product["rating"] = round(float(product["rating"]), 1)
        except (ValueError, TypeError):
            product["rating"] = None
    return product

def clean_products(products: list) -> list:
    cleaned = []
    for p in products:
        c = clean_product(p)
        if c and c.get("current_price") and c.get("title"):
            cleaned.append(c)
    skipped = len(products) - len(cleaned)
    if skipped:
        print(f"  ⚠️ Skipped {skipped} invalid products")
    return cleaned