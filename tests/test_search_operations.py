"""Тесты для модуля search_operations."""

from typing import Any, Dict, List

import pytest

from src.search_operations import process_bank_operations, process_bank_search


@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    """Фикстура: список транзакций для тестирования поиска."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "description": "Перевод со счета на счет",
        },
        {
            "id": 3,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "description": "Оплата услуг",
        },
        {
            "id": 5,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "description": "Перевод организации",
        },
    ]


# -------- ТЕСТЫ ПОИСКА (process_bank_search) --------


def test_process_bank_search_found(transactions: List[Dict[str, Any]]) -> None:
    """Тест: поиск по описанию находит совпадения."""
    result = process_bank_search(transactions, "перевод")
    assert len(result) == 4


def test_process_bank_search_case_insensitive(transactions: List[Dict[str, Any]]) -> None:
    """Тест: поиск не зависит от регистра."""
    result = process_bank_search(transactions, "ПЕРЕВОД")
    assert len(result) == 4


def test_process_bank_search_not_found(transactions: List[Dict[str, Any]]) -> None:
    """Тест: поиск не находит совпадений."""
    result = process_bank_search(transactions, "ипотека")
    assert result == []


def test_process_bank_search_empty_search(transactions: List[Dict[str, Any]]) -> None:
    """Тест: пустая строка поиска возвращает весь список."""
    result = process_bank_search(transactions, "")
    assert len(result) == len(transactions)


def test_process_bank_search_special_chars(transactions: List[Dict[str, Any]]) -> None:
    """Тест: поиск со спецсимволами (re.escape)."""
    result = process_bank_search(transactions, "услуг.")
    assert result == []


# -------- ТЕСТЫ ПОДСЧЕТА (process_bank_operations) --------


def test_process_bank_operations(transactions: List[Dict[str, Any]]) -> None:
    """Тест: правильный подсчет категорий."""
    categories = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Оплата услуг",
    ]
    result = process_bank_operations(transactions, categories)

    assert result["Перевод организации"] == 2
    assert result["Перевод со счета на счет"] == 1
    assert result["Перевод с карты на карту"] == 1
    assert result["Оплата услуг"] == 1


def test_process_bank_operations_unknown_category(transactions: List[Dict[str, Any]]) -> None:
    """Тест: категория, которой нет в данных, получает 0."""
    categories = ["Неизвестная категория"]
    result = process_bank_operations(transactions, categories)

    assert result["Неизвестная категория"] == 0


def test_process_bank_operations_empty_categories(transactions: List[Dict[str, Any]]) -> None:
    """Тест: пустой список категорий."""
    result = process_bank_operations(transactions, [])
    assert result == {}
