"""Модуль для обработки данных банковских операций."""

from datetime import datetime
from typing import Any


def filter_by_state(transactions: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Функция принимает список словарей, содержащих информацию о банковских операциях,
    и возвращает новый список, содержащий только те операции, у которых значение
    ключа 'state' соответствует указанному.

    Args:
        transactions (list): Список словарей с данными операций.
        state (str): Значение для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        list: Новый список словарей, отфильтрованный по state.

    Raises:
        ValueError: Если список пуст или не содержит операций.
        TypeError: Если аргументы имеют неверный тип.

    """
    # Проверка типа аргумента transactions
    if not isinstance(transactions, list):
        raise TypeError(f"transactions должен быть списком, получен {type(transactions).__name__}")

    # Проверка на пустой список
    if not transactions:
        raise ValueError("Список транзакций не может быть пустым")

    # Проверка типа аргумента state
    if not isinstance(state, str):
        raise TypeError(f"state должен быть строкой, получен {type(state).__name__}")

    # Создаем новый список с помощью list comprehension
    # Проходим по каждому словарю в списке и проверяем значение ключа 'state'
    filtered_list = [transaction for transaction in transactions if transaction.get("state") == state]

    # Проверяем, есть ли результат после фильтрации
    if not filtered_list:
        raise ValueError(f"Нет транзакций со статусом '{state}'")

    return filtered_list


def sort_by_date(transactions_list: list[dict[str, Any]], descending: bool = True) -> list[dict[str, Any]]:
    """
    Сортирует список словарей по дате.

    Функция принимает список словарей и возвращает новый список,
    отсортированный по дате (ключ 'date'). По умолчанию сортировка
    происходит по убыванию (сначала самые последние операции).

    Args:
        transactions_list (list[dict[str, object]]): Список словарей с транзакциями.
            Каждый словарь должен содержать ключ 'date' с датой в ISO формате.
        descending (bool): Порядок сортировки.
            True - по убыванию (сначала новые), False - по возрастанию (сначала старые).
            По умолчанию True.

    Returns:
        list[dict[str, object]]: Новый отсортированный список словарей.

    Raises:
        ValueError: Если список пуст.
        TypeError: Если transactions_list не является списком.

    """
    # Проверка типа аргумента
    if not isinstance(transactions_list, list):
        raise TypeError(f"transactions_list должен быть списком, получен {type(transactions_list).__name__}")

    # Проверка на пустой список
    if not transactions_list:
        raise ValueError("Список транзакций не может быть пустым")

    # Создаем копию списка, чтобы не изменять оригинал
    sorted_list = transactions_list.copy()

    # Сортируем список по дате
    # key=lambda x: datetime.fromisoformat(x["date"]) - извлекаем дату и преобразуем в datetime
    # reverse=descending - если descending=True, то сортируем по убыванию (сначала новые)
    sorted_list.sort(key=lambda x: datetime.fromisoformat(x["date"]), reverse=descending)

    return sorted_list
