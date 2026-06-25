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


"""ТЕСТЫ transaction_descriptions"""
def test_transaction_descriptions(transactions):
    """Тест: генератор описаний транзакций."""
    descriptions = transaction_descriptions(transactions)

    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    assert next(descriptions) == "Перевод организации"


def test_transaction_descriptions_empty():
    """Тест: генератор с пустым списком."""
    descriptions = transaction_descriptions([])

    with pytest.raises(StopIteration):
        next(descriptions)


def test_transaction_descriptions_missing_description(transactions):
    """Тест: транзакция без описания."""
    # Создаем транзакцию без ключа 'description'
    transactions_without_desc = [
        {"id": 1, "description": "Оплата"},
        {"id": 2},  # без description
        {"id": 3, "description": "Перевод"},
    ]

    descriptions = transaction_descriptions(transactions_without_desc)

    assert next(descriptions) == "Оплата"
    assert next(descriptions) == ""  # Пустая строка для отсутствующего описания
    assert next(descriptions) == "Перевод"