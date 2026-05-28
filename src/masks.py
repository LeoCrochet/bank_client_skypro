"""Модуль для маскировки номеров банковских карт и счетов."""


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Формат: XXXX XX** **** XXXX
    Пример: 1234 56** **** 1234

    Args:
        card_number (str): Номер карты в виде строки (16 цифр)

    Returns:
        str: Замаскированный номер карты

    Raises:
        ValueError: Если номер карты содержит не 16 цифр
    """
    # Удаляем все пробелы и проверяем длину
    clean_number = card_number.replace(" ", "")

    if not clean_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    if len(clean_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Маскируем номер: первые 6 цифр, затем **, затем последние 4 цифры
    masked = f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"

    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    Формат: **XXXX
    Пример: **1234

    Args:
        account_number (str): Номер счета в виде строки

    Returns:
        str: Замаскированный номер счета (только последние 4 цифры)

    Raises:
        ValueError: Если номер счета содержит менее 4 цифр
    """
    # Удаляем все пробелы
    clean_number = account_number.replace(" ", "")

    if not clean_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    if len(clean_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    # Показываем только последние 4 цифры, остальное маскируем
    masked = f"**{clean_number[-4:]}"

    return masked
