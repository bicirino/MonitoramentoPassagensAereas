import sqlite3
from pathlib import Path
from typing import Optional


class FlightPriceDB:
    def __init__(self, db_path: str = "flights.db") -> None:
        self.db_path = Path(db_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS flight_prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    origin TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    price REAL NOT NULL,
                    currency TEXT NOT NULL DEFAULT 'BRL',
                    checked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def insert_price(
        self,
        origin: str,
        destination: str,
        price: float,
        currency: str = "BRL",
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO flight_prices (origin, destination, price, currency)
                VALUES (?, ?, ?, ?)
                """,
                (origin, destination, price, currency),
            )

    def get_latest_price(self, origin: str, destination: str) -> Optional[float]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT price
                FROM flight_prices
                WHERE origin = ? AND destination = ?
                ORDER BY checked_at DESC, id DESC
                LIMIT 1
                """,
                (origin, destination),
            )
            row = cursor.fetchone()
            return float(row[0]) if row else None
