import pytest

from src.database.db_handler import FlightPriceDB
from src.exceptions import DatabaseError


def test_insert_and_get_latest_price(temp_db):
    """Testa inserção e recuperação do preço mais recente."""
    temp_db.insert_price(origin="GRU", destination="FLN", price=599.90)

    latest = temp_db.get_latest_price(origin="GRU", destination="FLN")

    assert latest == 599.90


def test_get_latest_price_returns_none_when_empty(temp_db):
    """Testa retorno None quando não há preços."""
    latest = temp_db.get_latest_price(origin="GRU", destination="FLN")
    assert latest is None


def test_insert_multiple_prices_returns_latest(temp_db):
    """Testa que get_latest_price retorna o mais recente após múltiplas inserções."""
    temp_db.insert_price(origin="GRU", destination="FLN", price=599.90)
    temp_db.insert_price(origin="GRU", destination="FLN", price=549.50)
    temp_db.insert_price(origin="GRU", destination="FLN", price=575.00)

    latest = temp_db.get_latest_price(origin="GRU", destination="FLN")

    # Deve retornar o último inserido
    assert latest == 575.00


def test_get_price_history(temp_db, sample_prices):
    """Testa recuperação do histórico de preços."""
    for price_data in sample_prices:
        temp_db.insert_price(**price_data)

    history = temp_db.get_price_history(origin="GRU", destination="FLN")

    assert len(history) == 2  # Dois preços para GRU-FLN
    assert history[0][0] == 549.50  # Último (mais recente)
    assert history[1][0] == 599.90


def test_get_statistics(temp_db):
    """Testa cálculo de estatísticas."""
    prices = [599.90, 549.50, 575.00, 600.00]
    for price in prices:
        temp_db.insert_price(origin="GRU", destination="FLN", price=price)

    stats = temp_db.get_statistics(origin="GRU", destination="FLN")

    assert stats["min_price"] == min(prices)
    assert stats["max_price"] == max(prices)
    assert stats["avg_price"] == round(sum(prices) / len(prices), 2)
    assert stats["total_records"] == len(prices)


def test_clear_old_records(temp_db):
    """Testa limpeza de registros antigos."""
    # Inserir registros
    temp_db.insert_price(origin="GRU", destination="FLN", price=599.90)
    temp_db.insert_price(origin="GRU", destination="FLN", price=549.50)

    # Limpar records com 0 dias (remove todos)
    deleted = temp_db.clear_old_records(days=0)

    assert deleted == 2
    assert temp_db.get_latest_price(origin="GRU", destination="FLN") is None


def test_different_routes(temp_db):
    """Testa que diferentes rotas não se misturam."""
    temp_db.insert_price(origin="GRU", destination="FLN", price=599.90)
    temp_db.insert_price(origin="GRU", destination="SSA", price=750.00)
    temp_db.insert_price(origin="GIG", destination="FLN", price=620.75)

    gru_fln = temp_db.get_latest_price(origin="GRU", destination="FLN")
    gru_ssa = temp_db.get_latest_price(origin="GRU", destination="SSA")
    gig_fln = temp_db.get_latest_price(origin="GIG", destination="FLN")

    assert gru_fln == 599.90
    assert gru_ssa == 750.00
    assert gig_fln == 620.75
