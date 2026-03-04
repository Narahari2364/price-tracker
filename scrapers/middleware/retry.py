import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from scrapers.middleware.user_agent import get_headers

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.exceptions.RequestException,))
)
def fetch_page(url, timeout=15):
    response = requests.get(url, headers=get_headers(), timeout=timeout)
    response.raise_for_status()
    return response