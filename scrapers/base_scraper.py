from abc import ABC, abstractmethod
from urllib.robotparser import RobotFileParser
import requests

class BaseScraper(ABC):
    def __init__(self, base_url, source_name):
        self.base_url = base_url
        self.source_name = source_name
        self._robots_parser = None

    def can_scrape(self, url):
        try:
            if self._robots_parser is None:
                self._robots_parser = RobotFileParser()
                self._robots_parser.set_url(f"{self.base_url}/robots.txt")
                self._robots_parser.read()
            return self._robots_parser.can_fetch("*", url)
        except Exception:
            return True

    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def parse_product(self, data):
        pass