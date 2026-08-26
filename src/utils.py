"""Модуль с утилитами для работы с данными."""

import json
import logging
import os
from typing import Any, Dict, List


# -------- НАСТРОЙКА ЛОГГЕРА --------

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Создаем директорию logs, если её нет
os.makedirs("logs", exist_ok=True)

# Очищаем файл лога при запуске (перезапись)
if os.path.exists("logs/utils.log"):
    with open("logs/utils.log", "w") as f:
        pass

# Настройка обработчика для записи в файл
file_handler = logging.FileHandler("logs/utils.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

# Формат лога: время | модуль | уровень | сообщение
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str): Путь до JSON-файла.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
    """
    logger.info(f"Начало чтения файла: {file_path}")

    # Проверяем существование и размер файла
    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден: {file_path}")
        return []

    if os.path.getsize(file_path) == 0:
        logger.warning(f"Файл пустой: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        logger.info(f"Файл успешно прочитан: {file_path}")

        if not isinstance(data, list):
            logger.error(f"Данные в файле не являются списком: {type(data).__name__}")
            return []

        logger.info(f"Количество транзакций в файле: {len(data)}")
        return data

    except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError) as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {type(e).__name__} - {e}")
        return []
