"""Тесты для модуля widget."""

import pytest
from src.widget import mask_account_card, get_date


# -------- ФИКСТУРЫ --------

@pytest.fixture
def card_test_data() -> list:
    """Фикстура: данные для тестирования карт."""
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Visa 7000792289606361", "Visa 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
    ]


@pytest.fixture
def account_test_data() -> list:
    """Фикстура: данные для тестирования счетов."""
    return [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("счет 73654108430135874305", "счет **4305"),
        ("Счет 1234567890", "Счет **7890"),
        ("Счет 1234", "Счет **1234"),
    ]


@pytest.fixture
def invalid_widget_inputs() -> list:
    """Фикстура: некорректные входные данные."""
    return [
        "",                                      # пустая строка
        "VisaPlatinum7000792289606361",          # без пробела
        "Visa Platinum",                         # только название
        "7000792289606361",                      # только номер
        "Visa 123456789012345",                  # короткий номер
        "Visa 1234abcd90123456",                 # буквы в номере
        "Счет 123",                              # короткий счет
        "Счет 1234abcd",                         # буквы в счете
    ]


@pytest.fixture
def date_test_data() -> list:
    """Фикстура: корректные даты."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11T02:26:18", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("2024-02-29T10:30:45.123456", "29.02.2024"),  # високосный год
        ("2024-12-31T23:59:59", "31.12.2024"),
    ]


@pytest.fixture
def invalid_date_inputs() -> list:
    """Фикстура: некорректные даты."""
    return [
        "",
        "11.03.2024",
        "2024/03/11",
        "2024-13-01",
        "2024-02-30",
        "not a date",
    ]


# -------- ТЕСТЫ ДЛЯ mask_account_card --------

def test_mask_account_card_card_types(card_test_data: list) -> None:
    """Тест: распознавание и маскировка карт."""
    for input_data, expected in card_test_data:
        assert mask_account_card(input_data) == expected


def test_mask_account_card_account_types(account_test_data: list) -> None:
    """Тест: распознавание и маскировка счетов."""
    for input_data, expected in account_test_data:
        assert mask_account_card(input_data) == expected


@pytest.mark.parametrize("input_data, expected_error", [
    ("", "Некорректный формат строки"),
    ("VisaPlatinum7000792289606361", "Некорректный формат строки"),
    ("Visa Platinum", "Номер карты должен содержать только цифры"),
    ("7000792289606361", "Некорректный формат строки"),
    ("Visa 123456789012345", "Номер карты должен содержать 16 цифр"),
    ("Visa 1234abcd90123456", "Номер карты должен содержать только цифры"),
    ("Счет 123", "Номер счета должен содержать минимум 4 цифры"),
    ("Счет 1234abcd", "Номер счета должен содержать только цифры"),
])
def test_mask_account_card_invalid(input_data: str, expected_error: str) -> None:
    """Тест: обработка некорректных входных данных."""
    with pytest.raises(ValueError, match=expected_error):
        mask_account_card(input_data)


# -------- ТЕСТЫ ДЛЯ get_date --------

def test_get_date_valid(date_test_data: list) -> None:
    """Тест: корректное преобразование даты."""
    for date_str, expected in date_test_data:
        assert get_date(date_str) == expected


@pytest.mark.parametrize("date_str", [
    "",
    "11.03.2024",
    "2024/03/11",
    "2024-13-01",
    "2024-02-30",
    "not a date",
])
def test_get_date_invalid(date_str: str) -> None:
    """Тест: обработка некорректных дат."""
    with pytest.raises(ValueError, match="Некорректный формат даты"):
        get_date(date_str)


def test_get_date_format() -> None:
    """Тест: проверка формата выходной даты."""
    result = get_date("2024-03-11T02:26:18.671407")
    parts = result.split(".")
    assert len(parts) == 3
    assert len(parts[0]) == 2  # день
    assert len(parts[1]) == 2  # месяц
    assert len(parts[2]) == 4  # год
    assert all(p.isdigit() for p in parts)


def test_get_date_edge_cases() -> None:
    """Тест: граничные случаи дат."""
    assert get_date("2024-01-01T00:00:00") == "01.01.2024"
    assert get_date("2024-12-31T23:59:59") == "31.12.2024"
    assert get_date("2024-02-29T12:00:00") == "29.02.2024"