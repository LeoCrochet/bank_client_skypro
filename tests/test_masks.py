"""Тесты для модуля masks."""

import pytest
from src.masks import get_mask_card_number


@pytest.mark.parametrize("card_number, expected", [
    # Стандартные корректные номера
    ("1234567890123456", "1234 56** **** 3456"),
    ("1111222233334444", "1111 22** **** 4444"),
    ("0000000000000000", "0000 00** **** 0000"),
    ("9999999999999999", "9999 99** **** 9999"),

    # Номера с пробелами и табуляцией
    ("1234 5678 9012 3456", "1234 56** **** 3456"),
    ("1234  5678  9012  3456", "1234 56** **** 3456"),
    ("  1234567890123456", "1234 56** **** 3456"),
    ("1234567890123456  ", "1234 56** **** 3456"),
    ("1234\t5678\t9012\t3456", "1234 56** **** 3456"),
])
def test_valid_card_numbers(card_number: str, expected: str) -> None:
    """Тест: корректные номера карт."""
    result = get_mask_card_number(card_number)
    assert result == expected


@pytest.mark.parametrize("card_number", [
    # Неверная длина
    "123456789012345",  # 15 цифр
    "12345678901234567",  # 17 цифр
    "1234",  # 4 цифры
    "001234567890",  # 12 цифр с ведущими нулями
    "1234 5678 9012 345",  # 15 цифр с пробелами
    "1234 5678 9012 34567",  # 17 цифр с пробелами
])
def test_invalid_card_length(card_number: str) -> None:
    """Тест: номера карт с неверной длиной."""
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(card_number)


@pytest.mark.parametrize("card_number", [
    # Символы, не являющиеся цифрами
    "1234abcd90123456",  # буквы
    "1234-5678-9012-3456",  # дефисы
    "1234.5678.9012.3456",  # точки
    "1234/5678/9012/3456",  # слеши
    "12345678\n90123456",  # новая строка
    "abcdefghijklmnop",  # только буквы
    "1234abcd5678efgh",  # смесь букв и цифр
])
def test_invalid_card_characters(card_number: str) -> None:
    """Тест: номера карт с недопустимыми символами."""
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number(card_number)