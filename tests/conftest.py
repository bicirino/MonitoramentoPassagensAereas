import os
import tempfile
from pathlib import Path

import pytest

from src.database.db_handler import FlightPriceDB


@pytest.fixture
def temp_db():
    """Cria um banco de dados temporário para testes."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
        db_path = f.name

    db = FlightPriceDB(db_path)
    yield db

    # Limpeza
    try:
        Path(db_path).unlink()
    except FileNotFoundError:
        pass


@pytest.fixture
def sample_prices():
    """Dados de amostra para testes."""
    return [
        {"origin": "GRU", "destination": "FLN", "price": 599.90},
        {"origin": "GRU", "destination": "FLN", "price": 549.50},
        {"origin": "GRU", "destination": "SSA", "price": 750.00},
        {"origin": "GIG", "destination": "FLN", "price": 620.75},
    ]


@pytest.fixture(autouse=True)
def reset_env():
    """Reset das variáveis de ambiente após cada teste."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)
