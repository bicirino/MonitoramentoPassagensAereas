import logging
import smtplib
from email.message import EmailMessage
from typing import Optional

from src.constants import SMTP_TIMEOUT
from src.exceptions import EmailError


class EmailService:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logger = logger or logging.getLogger(__name__)

    def send_alert(self, to_email: str, subject: str, body: str) -> bool:
        """Envia um e-mail de alerta. Retorna True se bem-sucedido."""
        try:
            message = EmailMessage()
            message["From"] = self.username
            message["To"] = to_email
            message["Subject"] = subject
            message.set_content(body, subtype="plain")

            # Adicionar versão HTML para melhor apresentação
            html_body = body.replace("\n", "<br>")
            message.add_alternative(f"<html><body><p>{html_body}</p></body></html>", subtype="html")

            self.logger.debug(f"Conectando ao servidor SMTP {self.host}:{self.port}")

            with smtplib.SMTP(self.host, self.port, timeout=SMTP_TIMEOUT) as server:
                server.starttls()
                self.logger.debug("Autenticando...")
                server.login(self.username, self.password)
                self.logger.debug(f"Enviando e-mail para {to_email}")
                server.send_message(message)

            self.logger.info(f"✓ Alerta enviado com sucesso para {to_email}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            self.logger.error(f"Erro de autenticação SMTP: {e}")
            raise EmailError(f"Erro ao autenticar no servidor SMTP: {e}")
        except smtplib.SMTPException as e:
            self.logger.error(f"Erro SMTP: {e}")
            raise EmailError(f"Erro ao enviar e-mail via SMTP: {e}")
        except Exception as e:
            self.logger.error(f"Erro inesperado ao enviar e-mail: {e}")
            raise EmailError(f"Erro inesperado ao enviar e-mail: {e}")

    def test_connection(self) -> bool:
        """Testa a conexão com o servidor SMTP."""
        try:
            self.logger.info("Testando conexão com servidor SMTP...")
            with smtplib.SMTP(self.host, self.port, timeout=SMTP_TIMEOUT) as server:
                server.starttls()
                server.login(self.username, self.password)
            self.logger.info("✓ Conexão SMTP bem-sucedida")
            return True
        except Exception as e:
            self.logger.error(f"✗ Erro de conexão SMTP: {e}")
            return False
