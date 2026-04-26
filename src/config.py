"""Gerenciamento centralizado de configurações."""

import os
import re
from typing import Optional

from dotenv import load_dotenv

from src.constants import (
    AIRPORT_CODE_PATTERN,
    DEFAULT_CURRENCY,
    DEFAULT_HEADLESS,
    SMTP_DEFAULT_HOST,
    SMTP_DEFAULT_PORT,
)
from src.exceptions import ConfigurationError


class Config:
    """Classe para gerenciar configurações do aplicativo."""

    def __init__(self) -> None:
        load_dotenv()
        self._validate_and_load()

    def _validate_and_load(self) -> None:
        """Valida e carrega todas as configurações necessárias."""
        # Busca
        self.origin = self._get_airport_code("ORIGIN", "GRU")
        self.destination = self._get_airport_code("DESTINATION", "FLN")
        self.target_price = self._get_positive_float("TARGET_PRICE", 650.0)

        # E-mail
        self.email_host = os.getenv("EMAIL_HOST", SMTP_DEFAULT_HOST)
        self.email_port = self._get_positive_int("EMAIL_PORT", SMTP_DEFAULT_PORT)
        self.email_user = os.getenv("EMAIL_USER", "")
        self.email_pass = os.getenv("EMAIL_PASS", "")
        self.email_to = os.getenv("EMAIL_TO", self.email_user)

        if not self.email_user or not self.email_pass:
            raise ConfigurationError(
                "EMAIL_USER e EMAIL_PASS não podem estar vazios"
            )

        # Execução
        self.headless = self._get_bool("HEADLESS", DEFAULT_HEADLESS)
        self.flights_url = os.getenv("FLIGHTS_URL", "")
        self.currency = os.getenv("CURRENCY", DEFAULT_CURRENCY)

        if not self.flights_url:
            raise ConfigurationError("FLIGHTS_URL é obrigatório")

    @staticmethod
    def _get_airport_code(key: str, default: str = "") -> str:
        """Obtém e valida código de aeroporto (3 letras maiúsculas)."""
        value = os.getenv(key, default).strip().upper()
        if not re.match(AIRPORT_CODE_PATTERN, value):
            raise ConfigurationError(
                f"{key} deve ser um código de aeroporto válido (3 letras, ex: GRU)"
            )
        return value

    @staticmethod
    def _get_positive_float(key: str, default: float = 0.0) -> float:
        """Obtém float positivo de variável de ambiente."""
        value_str = os.getenv(key, str(default))
        try:
            value = float(value_str)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            raise ConfigurationError(f"{key} deve ser um número positivo, recebido: {value_str}")

    @staticmethod
    def _get_positive_int(key: str, default: int = 0) -> int:
        """Obtém inteiro positivo de variável de ambiente."""
        value_str = os.getenv(key, str(default))
        try:
            value = int(value_str)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            raise ConfigurationError(f"{key} deve ser um inteiro positivo, recebido: {value_str}")

    @staticmethod
    def _get_bool(key: str, default: bool = True) -> bool:
        """Converte string em booleano."""
        value = os.getenv(key, str(default)).strip().lower()
        return value in {"1", "true", "yes", "on"}

    def to_dict(self) -> dict:
        """Retorna todas as configurações como dicionário."""
        return {
            "origin": self.origin,
            "destination": self.destination,
            "target_price": self.target_price,
            "email_host": self.email_host,
            "email_port": self.email_port,
            "email_user": self.email_user,
            "email_to": self.email_to,
            "headless": self.headless,
            "flights_url": self.flights_url,
            "currency": self.currency,
        }
