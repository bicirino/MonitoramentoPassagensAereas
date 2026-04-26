import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple

from src.constants import DB_PATH, DB_TIMEOUT
from src.exceptions import DatabaseError


class FlightPriceDB:
    def __init__(self, db_path: str = str(DB_PATH), logger: Optional[logging.Logger] = None) -> None:
        self.db_path = Path(db_path)
        self.logger = logger or logging.getLogger(__name__)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        """Cria uma conexão com o banco de dados."""
        try:
            conn = sqlite3.connect(str(self.db_path), timeout=DB_TIMEOUT)
            conn.row_factory = sqlite3.Row  # Retorna resultados como dicts
            return conn
        except sqlite3.Error as e:
            raise DatabaseError(f"Erro ao conectar ao banco de dados: {e}")

    def _initialize(self) -> None:
        """Inicializa o banco de dados criando a tabela se necessário."""
        try:
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
                # Criar índice para buscas rápidas
                conn.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_origin_destination 
                    ON flight_prices(origin, destination)
                    """
                )
                self.logger.debug("Banco de dados inicializado com sucesso")
        except sqlite3.Error as e:
            raise DatabaseError(f"Erro ao inicializar banco de dados: {e}")

    def insert_price(
        self,
        origin: str,
        destination: str,
        price: float,
        currency: str = "BRL",
    ) -> int:
        """Insere um novo preço no banco de dados. Retorna o ID inserido."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO flight_prices (origin, destination, price, currency)
                    VALUES (?, ?, ?, ?)
                    """,
                    (origin, destination, price, currency),
                )
                conn.commit()
                self.logger.debug(f"Preço inserido: {origin}-{destination} = R$ {price:.2f}")
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise DatabaseError(f"Erro ao inserir preço: {e}")

    def get_latest_price(self, origin: str, destination: str) -> Optional[float]:
        """Obtém o último preço registrado para uma rota."""
        try:
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
        except sqlite3.Error as e:
            raise DatabaseError(f"Erro ao buscar preço: {e}")

    def get_price_history(
        self,
        origin: str,
        destination: str,
        days: int = 7,
        limit: Optional[int] = None,
    ) -> List[Tuple[float, str]]:
        """Retorna histórico de preços dos últimos N dias."""
        try:
            with self._connect() as conn:
                since = datetime.now() - timedelta(days=days)
                query = """
                    SELECT price, checked_at
                    FROM flight_prices
                    WHERE origin = ? AND destination = ? AND checked_at >= ?
                    ORDER BY checked_at DESC
                """
                params = (origin, destination, since.isoformat())

                if limit:
                    query += " LIMIT ?"
                    params = params + (limit,)

                cursor = conn.execute(query, params)
                return [(row[0], row[1]) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            raise DatabaseError(f"Erro ao buscar histórico: {e}")

    def get_statistics(self, origin: str, destination: str, days: int = 7) -> dict:
        """Retorna estatísticas de preço para uma rota."""
        try:
            with self._connect() as conn:
                since = datetime.now() - timedelta(days=days)
                cursor = conn.execute(
                    """
                    SELECT 
                        MIN(price) as min_price,
                        MAX(price) as max_price,
                        AVG(price) as avg_price,
                        COUNT(*) as total_records
                    FROM flight_prices
                    WHERE origin = ? AND destination = ? AND checked_at >= ?
                    """,
                    (origin, destination, since.isoformat()),
                )
                row = cursor.fetchone()
                if row:
                    return {
                        "min_price": row[0],
                        "max_price": row[1],
                        "avg_price": round(row[2], 2) if row[2] else None,
                        "total_records": row[3],
                    }
                return {}
        except sqlite3.Error as e:
            raise DatabaseError(f"Erro ao buscar estatísticas: {e}")

    def clear_old_records(self, days: int = 90) -> int:
        """Remove registros com mais de N dias. Retorna quantidade deletada."""
        try:
            with self._connect() as conn:
                cutoff = datetime.now() - timedelta(days=days)
                cursor = conn.execute(
                    "DELETE FROM flight_prices WHERE checked_at < ?",
                    (cutoff.isoformat(),),
                )
                conn.commit()
                deleted = cursor.rowcount
                self.logger.info(f"Removidos {deleted} registros anteriores a {days} dias")
                return deleted
        except sqlite3.Error as e:
            raise DatabaseError(f"Erro ao limpar registros antigos: {e}")
