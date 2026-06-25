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