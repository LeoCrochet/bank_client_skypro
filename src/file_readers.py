import logging
import os

import pandas as pd

logger = logging.getLogger("file_readers")
logger.setLevel(logging.INFO)

os.makedirs("logs", exist_ok=True)

if os.path.exists("logs/file_readers.log"):
    with open("logs/file_readers.log", "w") as f:
        pass

file_handler = logging.FileHandler("logs/file_readers.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def read_transactions_from_csv(file_path):
    logger.info(f"Начало чтения CSV-файла: {file_path}")

    if not os.path.exists(file_path):
        logger.warning(f"CSV-файл не найден: {file_path}")
        return []

    if os.path.getsize(file_path) == 0:
        logger.warning(f"CSV-файл пустой: {file_path}")
        return []

    try:
        df = pd.read_csv(file_path, sep=";", encoding="utf-8")
        transactions = df.to_dict(orient="records")

        logger.info(f"CSV-файл успешно прочитан: {file_path}, транзакций: {len(transactions)}")
        return transactions

    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as e:
        logger.error(f"Ошибка при чтении CSV-файла {file_path}: {type(e).__name__} - {e}")
        return []


def read_transactions_from_excel(file_path):
    if not os.path.exists(file_path):
        logger.warning(f"Excel-файл не найден: {file_path}")
        return []

    if os.path.getsize(file_path) == 0:
        logger.warning(f"Excel-файл пустой: {file_path}")
        return []
    try:
        # ✅ Используем calamine вместо openpyxl
        df = pd.read_excel(file_path, engine="calamine")
        transactions = df.to_dict(orient="records")

        logger.info(f"Excel-файл успешно прочитан: {file_path}, транзакций: {len(transactions)}")
        return transactions

    except (ValueError, KeyError, UnicodeDecodeError) as e:
        logger.error(f"Ошибка при чтении Excel-файла {file_path}: {type(e).__name__} - {e}")
        return []
