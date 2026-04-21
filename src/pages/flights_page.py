import logging
import re
from typing import Optional

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class FlightsPage(BasePage):
    PRICE_PATTERN = re.compile(r"R\$\s?(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)")

    def __init__(self, page: Page, logger: Optional[logging.Logger] = None) -> None:
        super().__init__(page)
        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def parse_price_text(price_text: str) -> float:
        normalized = price_text.replace(".", "").replace(",", ".")
        return float(normalized)

    def open_search_page(self, flights_url: str) -> None:
        self.logger.info("Abrindo página de voos: %s", flights_url)
        self.goto(flights_url)

    def extract_lowest_price(self, wait_ms: int = 6000) -> Optional[float]:
        self.wait(wait_ms)
        html = self.page.content()
        matches = self.PRICE_PATTERN.findall(html)
        if not matches:
            self.logger.warning("Nenhum preço detectado na página.")
            return None

        prices = [self.parse_price_text(item) for item in matches]
        lowest = min(prices)
        self.logger.info("Menor preço detectado: R$ %.2f", lowest)
        return lowest
