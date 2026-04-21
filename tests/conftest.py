import pytest

from src.database.db_handler import FlightPriceDB


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_flights.db"
    return FlightPriceDB(str(db_file))
