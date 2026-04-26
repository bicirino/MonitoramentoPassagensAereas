"""Testes para o módulo de serviço de e-mail."""

from unittest.mock import MagicMock, patch

import pytest

from src.services.email_service import EmailService
from src.exceptions import EmailError


def test_email_service_initialization():
    """Testa inicialização do serviço de e-mail."""
    service = EmailService(
        host="smtp.gmail.com",
        port=587,
        username="test@gmail.com",
        password="testpass",
    )

    assert service.host == "smtp.gmail.com"
    assert service.port == 587
    assert service.username == "test@gmail.com"


def test_send_alert_success():
    """Testa envio bem-sucedido de alerta (mock)."""
    service = EmailService(
        host="smtp.gmail.com",
        port=587,
        username="test@gmail.com",
        password="testpass",
    )

    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = service.send_alert(
            to_email="recipient@gmail.com",
            subject="Test",
            body="Test body",
        )

        assert result is True
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()


def test_send_alert_auth_error():
    """Testa falha de autenticação."""
    service = EmailService(
        host="smtp.gmail.com",
        port=587,
        username="invalid@gmail.com",
        password="wrongpass",
    )

    with patch("smtplib.SMTP") as mock_smtp:
        import smtplib
        mock_smtp.return_value.__enter__.return_value.login.side_effect = (
            smtplib.SMTPAuthenticationError(535, "Authentication failed")
        )

        with pytest.raises(EmailError):
            service.send_alert(
                to_email="recipient@gmail.com",
                subject="Test",
                body="Test body",
            )


def test_parse_price_text():
    """Testa parsing de preços em diferentes formatos."""
    from src.pages.flights_page import FlightsPage

    assert FlightsPage.parse_price_text("1.234,56") == 1234.56
    assert FlightsPage.parse_price_text("99,99") == 99.99
    assert FlightsPage.parse_price_text("1000,00") == 1000.0