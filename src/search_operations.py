"""Модуль для поиска и подсчета банковских операций."""

import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по наличию строки поиска в описании (без учета регистра).

    Args:
        data (List[Dict[str, Any]]): Список словарей с транзакциями.
        search (str): Строка поиска.

    Returns:
        List[Dict[str, Any]]: Список отфильтрованных словарей.
    """
    if not search:
        return data

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []

    for transaction in data:
        description = transaction.get("description", "")
        if isinstance(description, str) and pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям (поле description).

    Args:
        data (List[Dict[str, Any]]): Список словарей с транзакциями.
        categories (List[str]): Список названий категорий для подсчета.

    Returns:
        Dict[str, int]: Словарь, где ключи — категории, значения — количество операций.
    """
    descriptions = [
        t.get("description") for t in data
        if t.get("description") in categories
    ]

    counts = Counter(descriptions)

    return {category: counts.get(category, 0) for category in categories}