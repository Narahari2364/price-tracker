import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from scheduler.jobs import run_scrape_job

def start_scheduler():
    scheduler = BlockingScheduler()

    scheduler.add_job(
        run_scrape_job,
        trigger=CronTrigger(hour=8, minute=0),
        id="daily_scrape",
        name="Daily Price Scrape",
        replace_existing=True
    )

    print("⏰ Scheduler started — scraping daily at 8:00 AM UTC")
    print("Press Ctrl+C to stop\\n")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\\n🛑 Scheduler stopped")
        scheduler.shutdown()

if __name__ == "__main__":
    start_scheduler()