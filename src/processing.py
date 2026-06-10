"""Модуль для обработки данных банковских операций."""


def filter_by_state(transactions: list, state: str = "EXECUTED") -> list:
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
    filtered_list = [
        transaction
        for transaction in transactions
        if transaction.get("state") == state
    ]

    # Проверяем, есть ли результат после фильтрации
    if not filtered_list:
        raise ValueError(f"Нет транзакций со статусом '{state}'")

    return filtered_list