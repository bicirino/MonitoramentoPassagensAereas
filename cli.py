#!/usr/bin/env python
"""Interface de linha de comando (CLI) para gerenciamento do projeto."""

import argparse
import sys

from src.config import Config
from src.database.db_handler import FlightPriceDB
from src.exceptions import ConfigurationError, DatabaseError
from src.services.email_service import EmailService
from src.utils.logger import get_logger


def cmd_test_email(args) -> int:
    """Testa conexão com servidor SMTP."""
    logger = get_logger("email-test")
    
    try:
        config = Config()
    except ConfigurationError as e:
        logger.error(f"Erro na configuração: {e}")
        return 1
    
    service = EmailService(
        host=config.email_host,
        port=config.email_port,
        username=config.email_user,
        password=config.email_pass,
        logger=logger,
    )
    
    if service.test_connection():
        return 0
    else:
        return 1


def cmd_show_stats(args) -> int:
    """Exibe estatísticas de preços."""
    logger = get_logger("stats")
    
    try:
        config = Config()
        db = FlightPriceDB(logger=logger)
    except ConfigurationError as e:
        logger.error(f"Erro na configuração: {e}")
        return 1
    except DatabaseError as e:
        logger.error(f"Erro no banco de dados: {e}")
        return 1
    
    stats = db.get_statistics(
        origin=config.origin,
        destination=config.destination,
        days=args.days,
    )
    
    if not stats:
        logger.info(f"Sem dados para {config.origin} → {config.destination} nos últimos {args.days} dias")
        return 0
    
    logger.info("=" * 60)
    logger.info(f"📊 Estatísticas: {config.origin} → {config.destination}")
    logger.info(f"   Período: Últimos {args.days} dias")
    logger.info("=" * 60)
    logger.info(f"   Menor preço:     R$ {stats['min_price']:.2f}")
    logger.info(f"   Maior preço:     R$ {stats['max_price']:.2f}")
    logger.info(f"   Preço médio:     R$ {stats['avg_price']:.2f}")
    logger.info(f"   Registros:       {stats['total_records']}")
    logger.info("=" * 60)
    
    return 0


def cmd_show_history(args) -> int:
    """Exibe histórico de preços."""
    logger = get_logger("history")
    
    try:
        config = Config()
        db = FlightPriceDB(logger=logger)
    except ConfigurationError as e:
        logger.error(f"Erro na configuração: {e}")
        return 1
    except DatabaseError as e:
        logger.error(f"Erro no banco de dados: {e}")
        return 1
    
    history = db.get_price_history(
        origin=config.origin,
        destination=config.destination,
        days=args.days,
        limit=args.limit,
    )
    
    if not history:
        logger.info(f"Sem dados para {config.origin} → {config.destination}")
        return 0
    
    logger.info("=" * 60)
    logger.info(f"📈 Histórico: {config.origin} → {config.destination}")
    logger.info("=" * 60)
    
    for price, timestamp in history:
        logger.info(f"   R$ {price:>8.2f}  |  {timestamp}")
    
    logger.info("=" * 60)
    return 0


def cmd_clear_old(args) -> int:
    """Limpa registros antigos do banco."""
    logger = get_logger("clear")
    
    try:
        db = FlightPriceDB(logger=logger)
    except DatabaseError as e:
        logger.error(f"Erro no banco de dados: {e}")
        return 1
    
    deleted = db.clear_old_records(days=args.days)
    logger.info(f"✓ Removidos {deleted} registros com mais de {args.days} dias")
    
    return 0


def main() -> int:
    """Função principal da CLI."""
    parser = argparse.ArgumentParser(
        description="🛠️  CLI para Monitor de Passagens Aéreas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s test-email          # Testa conexão SMTP
  %(prog)s stats -d 30         # Mostra stats dos últimos 30 dias
  %(prog)s history -d 7 -l 10  # Mostra histórico dos 7 últimos dias (max 10)
  %(prog)s clear -d 90         # Remove dados com mais de 90 dias
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")
    
    # Comando: test-email
    subparsers.add_parser(
        "test-email",
        help="Testa conexão com servidor SMTP",
    ).set_defaults(func=cmd_test_email)
    
    # Comando: stats
    stats_parser = subparsers.add_parser(
        "stats",
        help="Exibe estatísticas de preços",
    )
    stats_parser.add_argument("-d", "--days", type=int, default=7, help="Número de dias (padrão: 7)")
    stats_parser.set_defaults(func=cmd_show_stats)
    
    # Comando: history
    history_parser = subparsers.add_parser(
        "history",
        help="Exibe histórico de preços",
    )
    history_parser.add_argument("-d", "--days", type=int, default=30, help="Número de dias (padrão: 30)")
    history_parser.add_argument("-l", "--limit", type=int, default=None, help="Máximo de registros a exibir")
    history_parser.set_defaults(func=cmd_show_history)
    
    # Comando: clear
    clear_parser = subparsers.add_parser(
        "clear",
        help="Limpa registros antigos",
    )
    clear_parser.add_argument("-d", "--days", type=int, default=90, help="Remover dados com mais de N dias (padrão: 90)")
    clear_parser.set_defaults(func=cmd_clear_old)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
