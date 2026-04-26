"""Ponto de entrada principal do sistema de monitoramento de passagens aéreas."""

import sys
import logging

from playwright.sync_api import sync_playwright

from src.config import Config
from src.database.db_handler import FlightPriceDB
from src.exceptions import ConfigurationError, DatabaseError, EmailError, ScraperError, FlightWatcherException
from src.pages.flights_page import FlightsPage
from src.services.email_service import EmailService
from src.utils.logger import get_logger


def main() -> int:
    """Função principal do aplicativo.
    
    Retorna:
        0: Sucesso
        1: Erro de configuração
        2: Erro de scraping
        3: Erro de banco de dados
        4: Erro de e-mail
    """
    logger = get_logger()

    try:
        # Carregar configuração
        logger.info("=" * 60)
        logger.info("🚀 Iniciando Monitor de Passagens Aéreas")
        logger.info("=" * 60)

        config = Config()
        logger.info("✓ Configuração carregada com sucesso")
        logger.debug(f"Configurações: {config.to_dict()}")

        # Inicializar banco de dados
        db = FlightPriceDB(logger=logger)
        logger.info("✓ Banco de dados inicializado")

        # Iniciar browser e scraping
        logger.info(f"📍 Monitorando rota: {config.origin} → {config.destination}")
        logger.info(f"💰 Preço alvo: R$ {config.target_price:.2f}")

        current_price = None
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=config.headless)
            page = browser.new_page()

            try:
                flights_page = FlightsPage(page, logger=logger)
                flights_page.open_search_page(config.flights_url)
                current_price = flights_page.extract_lowest_price()
                logger.debug(f"URL atual: {flights_page.get_page_url()}")
            finally:
                browser.close()
                logger.info("✓ Browser encerrado")

        # Validar preço extraído
        if current_price is None:
            logger.warning("⚠️  Execução finalizada - nenhum preço válido foi encontrado")
            return 0

        # Salvar preço no banco
        try:
            price_id = db.insert_price(
                origin=config.origin,
                destination=config.destination,
                price=current_price,
                currency=config.currency,
            )
            logger.info(
                f"✓ Preço salvo no banco | "
                f"rota={config.origin}-{config.destination} | "
                f"valor=R$ {current_price:.2f} | ID={price_id}"
            )
        except DatabaseError as e:
            logger.error(f"Erro ao salvar preço: {e}")
            return 3

        # Verificar se atingiu preço-alvo
        if current_price <= config.target_price:
            logger.info("🎯 Preço alvo atingido!")
            logger.info(f"📧 Enviando alerta de preço...")

            try:
                email_service = EmailService(
                    host=config.email_host,
                    port=config.email_port,
                    username=config.email_user,
                    password=config.email_pass,
                    logger=logger,
                )

                subject = f"✈️ [ALERTA] Passagem {config.origin} → {config.destination}"
                body = (
                    f"🎉 Alerta de Preço de Passagem\n\n"
                    f"Rota: {config.origin} → {config.destination}\n"
                    f"Preço encontrado: R$ {current_price:.2f}\n"
                    f"Preço alvo: R$ {config.target_price:.2f}\n"
                    f"Diferença: R$ {config.target_price - current_price:.2f} de desconto!\n\n"
                    f"Verifique os detalhes em: {config.flights_url}"
                )

                email_service.send_alert(
                    to_email=config.email_to,
                    subject=subject,
                    body=body,
                )
            except EmailError as e:
                logger.error(f"❌ Falha ao enviar e-mail: {e}")
                return 4
        else:
            logger.info(
                f"ℹ️  Preço acima do alvo | "
                f"Diferença: R$ {current_price - config.target_price:.2f}"
            )

        logger.info("=" * 60)
        logger.info("✓ Execução finalizada com sucesso")
        logger.info("=" * 60)
        return 0

    except ConfigurationError as e:
        logger.error(f"❌ Erro de configuração: {e}")
        logger.info("💡 Dica: Verifique o arquivo .env e execute 'cp .env.example .env'")
        return 1

    except ScraperError as e:
        logger.error(f"❌ Erro ao fazer scraping: {e}")
        return 2

    except FlightWatcherException as e:
        logger.error(f"❌ Erro no aplicativo: {e}")
        return 1

    except KeyboardInterrupt:
        logger.warning("⚠️  Execução interrompida pelo usuário")
        return 1

    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
