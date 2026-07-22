import json
import os
from typing import Any, Dict, List


def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str): Путь до JSON-файла.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
    """

    # Проверяем существование и размер файла.
    # Если файла нет, или он пустой возвращаем пустой список
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []

    return data if isinstance(data, list) else []
