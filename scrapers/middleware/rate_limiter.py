import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

def polite_delay():
    min_delay = float(os.getenv("SCRAPE_DELAY_MIN", 1))
    max_delay = float(os.getenv("SCRAPE_DELAY_MAX", 3))
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def short_delay():
    time.sleep(random.uniform(0.5, 1.0))