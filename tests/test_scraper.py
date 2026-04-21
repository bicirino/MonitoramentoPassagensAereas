import os

import pytest
from playwright.sync_api import sync_playwright

from src.pages.flights_page import FlightsPage


def test_parse_price_text_br_format():
    value = FlightsPage.parse_price_text("1.234,56")
    assert value == 1234.56


@pytest.mark.skipif(
    os.getenv("RUN_E2E") != "1",
    reason="Teste E2E opcional. Defina RUN_E2E=1 para executar.",
)
def test_e2e_page_load():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.google.com/travel/flights", wait_until="domcontentloaded")
        assert "flights" in page.url
        browser.close()
