"""Exceções customizadas do projeto."""


class FlightWatcherException(Exception):
    """Exceção base do projeto."""
    pass


class ConfigurationError(FlightWatcherException):
    """Erro na configuração de variáveis de ambiente."""
    pass


class DatabaseError(FlightWatcherException):
    """Erro ao acessar o banco de dados."""
    pass


class ScraperError(FlightWatcherException):
    """Erro durante scraping."""
    pass


class EmailError(FlightWatcherException):
    """Erro ao enviar e-mail."""
    pass
