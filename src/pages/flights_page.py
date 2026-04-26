import logging
import re
import time
from typing import Optional

from playwright.sync_api import Page

from src.constants import BROWSER_WAIT_TIME, PRICE_PATTERN, RETRY_ATTEMPTS, RETRY_DELAY
from src.exceptions import ScraperError
from src.pages.base_page import BasePage


class FlightsPage(BasePage):
    PRICE_PATTERN = re.compile(PRICE_PATTERN)

    def __init__(self, page: Page, logger: Optional[logging.Logger] = None) -> None:
        super().__init__(page, logger=logger)

    @staticmethod
    def parse_price_text(price_text: str) -> float:
        """Converte formato de preço brasileiro para float."""
        normalized = price_text.replace(".", "").replace(",", ".")
        return float(normalized)

    def open_search_page(self, flights_url: str, retry: int = 0) -> None:
        """Abre a página de busca com retry automático."""
        try:
            self.logger.info(f"Abrindo página de voos (tentativa {retry + 1}/{RETRY_ATTEMPTS}): {flights_url}")
            self.goto(flights_url)
        except Exception as e:
            if retry < RETRY_ATTEMPTS - 1:
                self.logger.warning(f"Erro ao carregar página, tentando novamente em {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
                self.open_search_page(flights_url, retry + 1)
            else:
                raise ScraperError(f"Falha ao carregar página após {RETRY_ATTEMPTS} tentativas: {e}")

    def extract_lowest_price(self, wait_ms: int = BROWSER_WAIT_TIME) -> Optional[float]:
        """Extrai o menor preço da página com tratamento de erro."""
        try:
            self.wait(wait_ms)
            html = self.get_content()

            if not html:
                self.logger.warning("Conteúdo HTML vazio")
                return None

            matches = self.PRICE_PATTERN.findall(html)

            if not matches:
                self.logger.warning("Nenhum preço detectado na página")
                return None

            prices = [self.parse_price_text(item) for item in matches]
            lowest = min(prices)

            self.logger.info(f"Preços encontrados: {len(prices)} | Menor preço: R$ {lowest:.2f}")
            return lowest

        except Exception as e:
            self.logger.error(f"Erro ao extrair preço: {e}")
            raise ScraperError(f"Erro ao extrair preço: {e}")

    def get_page_title(self) -> str:
        """Retorna o título da página (útil para debug)."""
        return self.page.title()

    def get_page_url(self) -> str:
        """Retorna a URL atual da página."""
        return self.page.url
