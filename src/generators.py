def filter_by_currency(transactions: list[dict], currency: str):
    """
    Фильтрует транзакции по валюте. Возвращает итератор.

    Args:
        transactions (list[dict]): Список словарей с транзакциями.
        currency (str): Код валюты для фильтрации (например, "USD").

    Yields:
        dict: Транзакция с указанной валютой.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction

def transaction_descriptions(transactions: list[dict]):
    """
    Генератор, который возвращает описание каждой транзакции по очереди.

    Args:
        transactions (list[dict]): Список словарей с транзакциями.

    Yields:
        str: Описание транзакции.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int):
    """
    Генератор номеров банковских карт в заданном диапазоне.
    """
    if start < 1 or end > 9999999999999999 or start > end:
        raise ValueError("Некорректный диапазон")

    for number in range(start, end + 1):
        yield " ".join([f"{number:016d}"[i:i + 4] for i in range(0, 16, 4)])