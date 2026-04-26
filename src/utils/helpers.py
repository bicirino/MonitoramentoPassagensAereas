"""Funções utilitárias para análise de preços e operações gerais."""

import logging
from typing import List, Optional, Tuple


def calculate_price_change(old_price: float, new_price: float) -> float:
    """Calcula a mudança percentual entre dois preços.
    
    Args:
        old_price: Preço anterior
        new_price: Preço atual
        
    Returns:
        Percentual de mudança (positivo = aumento, negativo = redução)
    """
    if old_price == 0:
        return 0.0
    return ((new_price - old_price) / old_price) * 100


def is_price_significant_change(
    old_price: float,
    new_price: float,
    threshold_percent: float = 10.0,
) -> bool:
    """Verifica se a mudança de preço é significativa (maior que threshold).
    
    Args:
        old_price: Preço anterior
        new_price: Preço atual
        threshold_percent: Percentual mínimo para considerar significativo
        
    Returns:
        True se a mudança é significativa
    """
    change = abs(calculate_price_change(old_price, new_price))
    return change >= threshold_percent


def format_price(price: float, currency: str = "BRL") -> str:
    """Formata preço para exibição.
    
    Args:
        price: Preço em float
        currency: Código da moeda
        
    Returns:
        String formatada (ex: "R$ 1.234,56")
    """
    if currency == "BRL":
        return f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    elif currency == "USD":
        return f"US$ {price:,.2f}"
    else:
        return f"{price:,.2f} {currency}"


def get_price_trend(prices: List[float]) -> str:
    """Determina a tendência de preços baseado em lista de valores.
    
    Args:
        prices: Lista de preços em ordem cronológica
        
    Returns:
        "up" (subindo), "down" (caindo) ou "stable" (estável)
    """
    if len(prices) < 2:
        return "stable"
    
    first = prices[0]
    last = prices[-1]
    
    if last > first * 1.02:  # 2% de aumento
        return "up"
    elif last < first * 0.98:  # 2% de redução
        return "down"
    else:
        return "stable"


def get_trend_emoji(trend: str) -> str:
    """Retorna emoji para representar tendência."""
    trends = {
        "up": "📈",
        "down": "📉",
        "stable": "➡️",
    }
    return trends.get(trend, "❓")


def find_best_and_worst_price(
    price_history: List[Tuple[float, str]],
) -> Tuple[Optional[float], Optional[float]]:
    """Encontra melhor e pior preço do histórico.
    
    Args:
        price_history: Lista de tuplas (preço, timestamp)
        
    Returns:
        Tupla (melhor_preço, pior_preço)
    """
    if not price_history:
        return None, None
    
    prices = [p[0] for p in price_history]
    return min(prices), max(prices)


def estimate_savings(target_price: float, current_price: float) -> Tuple[float, float]:
    """Estima economia ao atingir preço-alvo.
    
    Args:
        target_price: Preço-alvo desejado
        current_price: Preço atual
        
    Returns:
        Tupla (economia_absoluta, economia_percentual)
    """
    if current_price <= target_price:
        return 0.0, 0.0
    
    savings = current_price - target_price
    percent = (savings / current_price) * 100
    return savings, percent
