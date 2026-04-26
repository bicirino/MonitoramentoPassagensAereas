import logging
from typing import Optional

from playwright.sync_api import Page

from src.constants import BROWSER_WAIT_TIME, DEFAULT_TIMEOUT


class BasePage:
    def __init__(self, page: Page, logger: Optional[logging.Logger] = None) -> None:
        self.page = page
        self.logger = logger or logging.getLogger(__name__)

    def goto(self, url: str, timeout_ms: int = DEFAULT_TIMEOUT) -> None:
        """Navega para uma URL com tratamento de erro."""
        self.logger.debug(f"Navegando para: {url}")
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            self.logger.debug(f"Página carregada com sucesso: {url}")
        except Exception as e:
            self.logger.error(f"Erro ao carregar {url}: {e}")
            raise

    def wait(self, milliseconds: int = BROWSER_WAIT_TIME) -> None:
        """Aguarda por tempo especificado em milissegundos."""
        self.page.wait_for_timeout(milliseconds)

    def get_content(self) -> str:
        """Retorna o conteúdo HTML da página."""
        return self.page.content()

    def close(self) -> None:
        """Fecha a página."""
        try:
            self.page.close()
            self.logger.debug("Página fechada com sucesso")
        except Exception as e:
            self.logger.warning(f"Erro ao fechar página: {e}")
