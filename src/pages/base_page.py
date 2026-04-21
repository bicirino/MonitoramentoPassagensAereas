from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str, timeout_ms: int = 60000) -> None:
        self.page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)

    def wait(self, milliseconds: int = 1500) -> None:
        self.page.wait_for_timeout(milliseconds)
