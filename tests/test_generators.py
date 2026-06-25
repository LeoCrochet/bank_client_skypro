import pytest
from src.generators import filter_by_currency
"""ТЕСТЫ filter_by_currency"""
def test_filter_by_currency(transactions):
    """Тест: фильтрация транзакций по валюте USD."""
    usd_transactions = list(filter_by_currency(transactions, "USD"))

    assert len(usd_transactions) == 2
    assert usd_transactions[0]["id"] == 939719570
    assert usd_transactions[1]["id"] == 142264268


def test_filter_by_currency_no_matches(transactions):
    """Тест: фильтрация по валюте, которой нет в транзакциях."""
    result = list(filter_by_currency(transactions, "EUR"))

    assert len(result) == 0


def test_filter_by_currency_iterator(transactions):
    """Тест: проверка работы итератора."""
    usd_transactions = filter_by_currency(transactions, "USD")

    first = next(usd_transactions)
    assert first["id"] == 939719570

    second = next(usd_transactions)
    assert second["id"] == 142264268