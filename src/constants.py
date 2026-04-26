"""Constantes do aplicativo."""

from pathlib import Path

# Diretórios
PROJECT_ROOT = Path(__file__).parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
DB_DIR = PROJECT_ROOT

# Banco de dados
DB_PATH = DB_DIR / "flights.db"
DB_TIMEOUT = 30  # segundos

# Browser
DEFAULT_TIMEOUT = 60000  # ms
BROWSER_WAIT_TIME = 6000  # ms para página carregar

# E-mail
SMTP_TIMEOUT = 30  # segundos
SMTP_DEFAULT_HOST = "smtp.gmail.com"
SMTP_DEFAULT_PORT = 587

# Padrões
PRICE_PATTERN = r"R\$\s?(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)"
AIRPORT_CODE_PATTERN = r"^[A-Z]{3}$"

# URLs
GOOGLE_FLIGHTS_URL = "https://www.google.com/travel/flights"

# Configurações padrão
DEFAULT_CURRENCY = "BRL"
DEFAULT_HEADLESS = True
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # segundos
