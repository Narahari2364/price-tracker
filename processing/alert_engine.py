from processing.price_analyzer import analyze_price_changes
from database.repositories.alert_repo import insert_alert

def run_alert_engine(job_id: str):
    print("\\n🚨 Running alert engine...")
    drops = analyze_price_changes(job_id)

    if not drops:
        print("  ℹ️ No significant price drops found")
        return []

    alerts_created = []
    for drop in drops:
        alert = insert_alert(
            product_id=drop["product_id"],
            price_before=drop["price_before"],
            price_after=drop["price_after"],
            drop_pct=drop["drop_pct"]
        )
        alerts_created.append(alert)
        print(f"  🔔 Alert: {drop['title'][:40]} dropped {drop['drop_pct']}%")

    print(f"\\n  ✅ Created {len(alerts_created)} alerts")
    return alerts_created