"""Тесты для модуля masks."""

import pytest

from src.masks import get_mask_account, get_mask_card_number

"""--------------------------------------"""
"""Тесты для функции get_mask_card_number"""
"""--------------------------------------"""


@pytest.mark.parametrize(
    "card_number, expected",
    [
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
    ],
)
def test_valid_card_numbers(card_number: str, expected: str) -> None:
    """Тест: корректные номера карт."""
    result = get_mask_card_number(card_number)
    assert result == expected


@pytest.mark.parametrize(
    "card_number",
    [
        # Неверная длина
        "123456789012345",  # 15 цифр
        "12345678901234567",  # 17 цифр
        "1234",  # 4 цифры
        "001234567890",  # 12 цифр с ведущими нулями
        "1234 5678 9012 345",  # 15 цифр с пробелами
        "1234 5678 9012 34567",  # 17 цифр с пробелами
    ],
)
def test_invalid_card_length(card_number: str) -> None:
    """Тест: номера карт с неверной длиной."""
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "card_number",
    [
        # Символы, не являющиеся цифрами
        "1234abcd90123456",  # буквы
        "1234-5678-9012-3456",  # дефисы
        "1234.5678.9012.3456",  # точки
        "1234/5678/9012/3456",  # слеши
        "12345678\n90123456",  # новая строка
        "abcdefghijklmnop",  # только буквы
        "1234abcd5678efgh",  # смесь букв и цифр
    ],
)
def test_invalid_card_characters(card_number: str) -> None:
    """Тест: номера карт с недопустимыми символами."""
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number(card_number)


"""----------------------------------"""
"""Тесты для функции get_mask_account"""
"""----------------------------------"""


def test_account_masking_does_not_reveal_full_number() -> None:
    """Тест: маскировка не раскрывает полный номер счета."""
    account_number_ = "1234567890"
    result = get_mask_account(account_number_)

    # Проверяем, что полный номер не отображается
    assert result != account_number_
    # Проверяем, что только последние 4 цифры видны
    assert result[-4:] == account_number_[-4:]
    assert result == "**7890"


@pytest.mark.parametrize(
    "account_number, expected",
    [
        # Проверка правильности маскировки для разных длин
        ("1234567890", "**7890"),
        ("12345", "**2345"),
        ("123456", "**3456"),
        ("1234567", "**4567"),
        ("12345678", "**5678"),
        ("123456789", "**6789"),
        ("1234567890", "**7890"),
        ("12345678901", "**8901"),
        ("123456789012", "**9012"),
        ("1234567890123", "**0123"),
        ("12345678901234", "**1234"),
        ("123456789012345", "**2345"),
        ("1234567890123456", "**3456"),
        ("12345678901234567", "**4567"),
        ("123456789012345678", "**5678"),
        ("1234567890123456789", "**6789"),
        ("12345678901234567890", "**7890"),
    ],
)
def test_account_masking_format(account_number: str, expected: str) -> None:
    """Тест: проверка правильности маскировки для разных длин."""
    result = get_mask_account(account_number)
    assert result == expected
    assert result.startswith("**")
    assert len(result) == 6  # ** + 4 цифры


@pytest.mark.parametrize(
    "account_number",
    [
        # Только пробелы в номере (после замены - пустая строка)
        "     ",
        "\t\t\t",
        "   \t   ",
        # Пробелы между цифрами, но всего 3 цифры
        "1 2 3",
        "12 3",
        "1 23",
    ],
)
def test_account_with_only_whitespace_or_too_few_digits(account_number: str) -> None:
    """Тест: номера счетов, состоящие только из пробелов или с недостаточным количеством цифр."""
    with pytest.raises(ValueError, match="Номер счета должен содержать минимум 4 цифры"):
        get_mask_account(account_number)


@pytest.mark.parametrize(
    "account",
    [
        # Символы, не являющиеся цифрами
        "1234abcd90123456",  # буквы
        "1234-5678-9012-3456",  # дефисы
        "1234.5678.9012.3456",  # точки
        "1234/5678/9012/3456",  # слеши
        "12345678\n90123456",  # новая строка
        "abcdefghijklmnop",  # только буквы
        "1234abcd5678efgh",  # смесь букв и цифр
    ],
)
def test_invalid_account_characters(account: str) -> None:
    """Тест: номера счета с недопустимыми символами."""
    with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
        get_mask_account(account)
