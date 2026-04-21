import smtplib
from email.message import EmailMessage


class EmailService:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def send_alert(self, to_email: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = self.username
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(self.host, self.port, timeout=30) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(message)
