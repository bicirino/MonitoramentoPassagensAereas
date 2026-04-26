"""Testes para o módulo de configuração."""

import os
import pytest

from src.config import Config
from src.exceptions import ConfigurationError


def test_config_loads_defaults():
    """Testa carregamento de configurações padrão."""
    # Limpar variáveis de ambiente
    for key in ["ORIGIN", "DESTINATION", "TARGET_PRICE", "EMAIL_USER", "EMAIL_PASS", "FLIGHTS_URL"]:
        os.environ.pop(key, None)

    os.environ["EMAIL_USER"] = "test@gmail.com"
    os.environ["EMAIL_PASS"] = "testpass"
    os.environ["FLIGHTS_URL"] = "https://example.com"

    config = Config()

    assert config.origin == "GRU"
    assert config.destination == "FLN"
    assert config.target_price == 650.0
    assert config.headless is True


def test_config_validates_airport_codes():
    """Testa validação de códigos de aeroporto."""
    os.environ["ORIGIN"] = "invalid"
    os.environ["EMAIL_USER"] = "test@gmail.com"
    os.environ["EMAIL_PASS"] = "testpass"
    os.environ["FLIGHTS_URL"] = "https://example.com"

    with pytest.raises(ConfigurationError):
        Config()


def test_config_validates_email_required():
    """Testa validação de e-mail obrigatório."""
    os.environ.pop("EMAIL_USER", None)
    os.environ.pop("EMAIL_PASS", None)
    os.environ["FLIGHTS_URL"] = "https://example.com"

    with pytest.raises(ConfigurationError):
        Config()


def test_config_validates_flights_url_required():
    """Testa validação de URL obrigatória."""
    os.environ.pop("FLIGHTS_URL", None)
    os.environ["EMAIL_USER"] = "test@gmail.com"
    os.environ["EMAIL_PASS"] = "testpass"

    with pytest.raises(ConfigurationError):
        Config()


def test_config_validates_positive_numbers():
    """Testa validação de números positivos."""
    os.environ["TARGET_PRICE"] = "-100"
    os.environ["EMAIL_USER"] = "test@gmail.com"
    os.environ["EMAIL_PASS"] = "testpass"
    os.environ["FLIGHTS_URL"] = "https://example.com"

    with pytest.raises(ConfigurationError):
        Config()


def test_config_to_dict():
    """Testa conversão de config para dicionário."""
    os.environ["ORIGIN"] = "GIG"
    os.environ["DESTINATION"] = "SSA"
    os.environ["TARGET_PRICE"] = "800"
    os.environ["EMAIL_USER"] = "test@gmail.com"
    os.environ["EMAIL_PASS"] = "testpass"
    os.environ["FLIGHTS_URL"] = "https://example.com"

    config = Config()
    config_dict = config.to_dict()

    assert config_dict["origin"] == "GIG"
    assert config_dict["destination"] == "SSA"
    assert config_dict["target_price"] == 800.0
    assert config_dict["email_user"] == "test@gmail.com"