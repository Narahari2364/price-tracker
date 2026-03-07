import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def load_template():
    template_path = os.path.join(
        os.path.dirname(__file__), "templates", "price_drop.html"
    )
    with open(template_path, "r") as f:
        return f.read()

def build_email(alert: dict, product: dict) -> str:
    template = load_template()
    saving = round(alert["price_before"] - alert["price_after"], 2)
    return (template
        .replace("{{title}}", product.get("title", "Unknown Product"))
        .replace("{{currency}}", product.get("currency", "GBP"))
        .replace("{{price_before}}", str(alert["price_before"]))
        .replace("{{price_after}}", str(alert["price_after"]))
        .replace("{{drop_pct}}", str(alert["drop_percentage"]))
        .replace("{{saving}}", str(saving))
        .replace("{{url}}", product.get("url", "#"))
    )

def send_alert_email(alert: dict, product: dict) -> bool:
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not all([sender, password, receiver]):
        print("  ⚠️ Email credentials not configured in .env")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🔥 Price Drop Alert: {product.get('title', '')[:50]}"
        msg["From"] = sender
        msg["To"] = receiver

        html_content = build_email(alert, product)
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())

        print(f"  📧 Email sent for: {product.get('title', '')[:40]}")
        return True

    except Exception as e:
        print(f"  ❌ Email failed: {e}")
        return False

def send_bulk_alerts(alerts: list) -> int:
    from database.repositories.product_repo import get_product_by_id
    from database.connection import get_db

    db = get_db()
    sent = 0

    for alert in alerts:
        product = get_product_by_id(alert["product_id"])
        if not product:
            continue
        success = send_alert_email(alert, product)
        if success:
            db.alerts.update_one(
                {"product_id": alert["product_id"], "notified": False},
                {"$set": {"notified": True}}
            )
            sent += 1

    return sent