"""Тесты для модуля processing."""

import pytest
from typing import List, Dict, Any
from src.processing import filter_by_state, sort_by_date

# -------- ФИКСТУРЫ --------


@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    """Фикстура: список транзакций для тестирования."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def transactions_with_same_date() -> List[Dict[str, Any]]:
    """Фикстура: транзакции с одинаковыми датами."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-01T15:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-01T12:00:00"},
    ]


@pytest.fixture
def transactions_no_state() -> List[Dict[str, Any]]:
    """Фикстура: транзакции без указанного статуса."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-02"},
        {"id": 3, "state": "CANCELED", "date": "2024-01-03"},
    ]


# -------- ТЕСТЫ ДЛЯ filter_by_state --------


def test_filter_by_state_executed(transactions: List[Dict[str, Any]]) -> None:
    """Тест: фильтрация по статусу 'EXECUTED'."""
    result = filter_by_state(transactions)
    assert len(result) == 2
    assert all(t["state"] == "EXECUTED" for t in result)
    assert result[0]["id"] == 41428829
    assert result[1]["id"] == 939719570


def test_filter_by_state_canceled(transactions: List[Dict[str, Any]]) -> None:
    """Тест: фильтрация по статусу 'CANCELED'."""
    result = filter_by_state(transactions, "CANCELED")
    assert len(result) == 2
    assert all(t["state"] == "CANCELED" for t in result)
    assert result[0]["id"] == 594226727
    assert result[1]["id"] == 615064591


def test_filter_by_state_no_matching(transactions_no_state: List[Dict[str, Any]]) -> None:
    """Тест: отсутствие транзакций с указанным статусом."""
    with pytest.raises(ValueError, match="Нет транзакций со статусом 'PENDING'"):
        filter_by_state(transactions_no_state, "PENDING")


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [41428829, 939719570]),
        ("CANCELED", [594226727, 615064591]),
    ],
)
def test_filter_by_state_parametrized(transactions: List[Dict[str, Any]], state: str, expected_ids: List[int]) -> None:
    """Тест: параметризованная фильтрация по разным статусам."""
    result = filter_by_state(transactions, state)
    assert len(result) == len(expected_ids)
    assert [t["id"] for t in result] == expected_ids


def test_filter_by_state_empty_list() -> None:
    """Тест: пустой список транзакций."""
    with pytest.raises(ValueError, match="Список транзакций не может быть пустым"):
        filter_by_state([])


def test_filter_by_state_invalid_type() -> None:
    """Тест: неверный тип данных."""
    with pytest.raises(TypeError, match="transactions должен быть списком, получен"):
        filter_by_state("not a list")  # type: ignore


# -------- ТЕСТЫ ДЛЯ sort_by_date --------


def test_sort_by_date_descending(transactions: List[Dict[str, Any]]) -> None:
    """Тест: сортировка по убыванию (новые сверху)."""
    result = sort_by_date(transactions)
    expected_ids = [41428829, 615064591, 594226727, 939719570]
    assert [t["id"] for t in result] == expected_ids


def test_sort_by_date_ascending(transactions: List[Dict[str, Any]]) -> None:
    """Тест: сортировка по возрастанию (старые сверху)."""
    result = sort_by_date(transactions, descending=False)
    expected_ids = [939719570, 594226727, 615064591, 41428829]
    assert [t["id"] for t in result] == expected_ids


def test_sort_by_date_same_dates(transactions_with_same_date: List[Dict[str, Any]]) -> None:
    """Тест: сортировка при одинаковых датах."""
    result = sort_by_date(transactions_with_same_date)
    expected_ids = [2, 3, 1]  # сортировка по времени
    assert [t["id"] for t in result] == expected_ids


def test_sort_by_date_returns_new_list(transactions: List[Dict[str, Any]]) -> None:
    """Тест: функция возвращает новый список, не изменяя оригинал."""
    original = transactions.copy()
    result = sort_by_date(transactions)
    assert result is not transactions
    assert transactions == original


def test_sort_by_date_empty_list() -> None:
    """Тест: пустой список."""
    with pytest.raises(ValueError, match="Список транзакций не может быть пустым"):
        sort_by_date([])


def test_sort_by_date_invalid_type() -> None:
    """Тест: неверный тип данных."""
    with pytest.raises(TypeError, match="transactions_list должен быть списком"):
        sort_by_date("not a list")  # type: ignore
