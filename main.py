import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from src.database.db_handler import FlightPriceDB
from src.pages.flights_page import FlightsPage
from src.services.email_service import EmailService
from src.utils.logger import get_logger


def as_bool(value: str, default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    load_dotenv()
    logger = get_logger()

    origin = os.getenv("ORIGIN", "GRU")
    destination = os.getenv("DESTINATION", "FLN")
    target_price = float(os.getenv("TARGET_PRICE", "650"))
    flights_url = os.getenv("FLIGHTS_URL", "https://www.google.com/travel/flights")
    headless = as_bool(os.getenv("HEADLESS", "true"), default=True)

    db = FlightPriceDB("flights.db")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        page = browser.new_page()

        flights_page = FlightsPage(page, logger=logger)
        flights_page.open_search_page(flights_url)
        current_price = flights_page.extract_lowest_price()
        browser.close()

    if current_price is None:
        logger.warning("Execução finalizada sem preço válido para registro.")
        return

    db.insert_price(origin=origin, destination=destination, price=current_price)
    logger.info(
        "Preço salvo no banco | rota=%s-%s | valor=R$ %.2f",
        origin,
        destination,
        current_price,
    )

    if current_price <= target_price:
        logger.info("Preço alvo atingido. Enviando alerta por e-mail.")
        email_service = EmailService(
            host=os.getenv("EMAIL_HOST", "smtp.gmail.com"),
            port=int(os.getenv("EMAIL_PORT", "587")),
            username=os.getenv("EMAIL_USER", ""),
            password=os.getenv("EMAIL_PASS", ""),
        )

        to_email = os.getenv("EMAIL_TO", os.getenv("EMAIL_USER", ""))
        email_service.send_alert(
            to_email=to_email,
            subject=f"[Alerta] Passagem {origin} -> {destination}",
            body=(
                f"O preço da rota {origin} -> {destination} atingiu R$ {current_price:.2f}.\n"
                f"Preço alvo configurado: R$ {target_price:.2f}."
            ),
        )
        logger.info("Alerta enviado para %s", to_email)
    else:
        logger.info("Preço ainda acima do alvo configurado.")


if __name__ == "__main__":
    main()
