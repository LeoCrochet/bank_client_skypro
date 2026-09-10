"""Тесты для модуля file_readers."""

import os
from typing import Any, Dict, List
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from src.file_readers import read_transactions_from_csv, read_transactions_from_excel


# -------- ФИКСТУРЫ --------

@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура: пример данных о транзакциях."""
    return [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": 3598919,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        },
    ]


# -------- ТЕСТЫ ДЛЯ CSV --------

@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
@patch("src.file_readers.pd.read_csv")
def test_read_csv_success(
    mock_read_csv: MagicMock,
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
    sample_transactions: List[Dict[str, Any]],
) -> None:
    """Тест: успешное чтение CSV-файла."""
    mock_exists.return_value = True
    mock_getsize.return_value = 1024

    mock_df = MagicMock()
    mock_df.to_dict.return_value = sample_transactions
    mock_read_csv.return_value = mock_df

    result = read_transactions_from_csv("data/transactions.csv")

    assert result == sample_transactions
    assert len(result) == 2
    mock_read_csv.assert_called_once_with(
        "data/transactions.csv", sep=";", encoding="utf-8"
    )


@patch("src.file_readers.os.path.exists")
def test_read_csv_file_not_found(mock_exists: MagicMock) -> None:
    """Тест: CSV-файл не найден."""
    mock_exists.return_value = False

    result = read_transactions_from_csv("non_existent.csv")

    assert result == []


@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
def test_read_csv_empty_file(
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Тест: пустой CSV-файл."""
    mock_exists.return_value = True
    mock_getsize.return_value = 0

    result = read_transactions_from_csv("empty.csv")

    assert result == []


@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
@patch("src.file_readers.pd.read_csv")
def test_read_csv_parser_error(
    mock_read_csv: MagicMock,
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Тест: ошибка парсинга CSV."""
    mock_exists.return_value = True
    mock_getsize.return_value = 1024
    mock_read_csv.side_effect = pd.errors.ParserError("Parser error")

    result = read_transactions_from_csv("invalid.csv")

    assert result == []


@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
@patch("src.file_readers.pd.read_csv")
def test_read_csv_empty_data_error(
    mock_read_csv: MagicMock,
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Тест: пустые данные в CSV."""
    mock_exists.return_value = True
    mock_getsize.return_value = 1024
    mock_read_csv.side_effect = pd.errors.EmptyDataError("No data")

    result = read_transactions_from_csv("empty_data.csv")

    assert result == []


@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
@patch("src.file_readers.pd.read_csv")
def test_read_csv_unicode_error(
    mock_read_csv: MagicMock,
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Тест: ошибка кодировки CSV."""
    mock_exists.return_value = True
    mock_getsize.return_value = 1024
    mock_read_csv.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "error")

    result = read_transactions_from_csv("invalid_encoding.csv")

    assert result == []


@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
@patch("src.file_readers.pd.read_csv")
def test_read_csv_empty_result(
    mock_read_csv: MagicMock,
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Тест: CSV с пустым результатом."""
    mock_exists.return_value = True
    mock_getsize.return_value = 1024

    mock_df = MagicMock()
    mock_df.to_dict.return_value = []
    mock_read_csv.return_value = mock_df

    result = read_transactions_from_csv("data/empty.csv")

    assert result == []


# -------- ТЕСТЫ ДЛЯ EXCEL --------

@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
@patch("src.file_readers.pd.read_excel")
def test_read_excel_success(
    mock_read_excel: MagicMock,
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
    sample_transactions: List[Dict[str, Any]],
) -> None:
    """Тест: успешное чтение Excel-файла."""
    mock_exists.return_value = True
    mock_getsize.return_value = 2048

    mock_df = MagicMock()
    mock_df.to_dict.return_value = sample_transactions
    mock_read_excel.return_value = mock_df

    result = read_transactions_from_excel("data/transactions_excel.xlsx")

    assert result == sample_transactions
    assert len(result) == 2
    mock_read_excel.assert_called_once_with(
        "data/transactions_excel.xlsx", engine="calamine"
    )


@patch("src.file_readers.os.path.exists")
def test_read_excel_file_not_found(mock_exists: MagicMock) -> None:
    """Тест: Excel-файл не найден."""
    mock_exists.return_value = False

    result = read_transactions_from_excel("non_existent.xlsx")

    assert result == []


@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
def test_read_excel_empty_file(
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Тест: пустой Excel-файл."""
    mock_exists.return_value = True
    mock_getsize.return_value = 0

    result = read_transactions_from_excel("empty.xlsx")

    assert result == []


@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
@patch("src.file_readers.pd.read_excel")
def test_read_excel_error(
    mock_read_excel: MagicMock,
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Тест: ошибка чтения Excel-файла."""
    mock_exists.return_value = True
    mock_getsize.return_value = 2048
    mock_read_excel.side_effect = ValueError("Invalid Excel file")

    result = read_transactions_from_excel("invalid.xlsx")

    assert result == []


@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
@patch("src.file_readers.pd.read_excel")
def test_read_excel_key_error(
    mock_read_excel: MagicMock,
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Тест: KeyError при чтении Excel."""
    mock_exists.return_value = True
    mock_getsize.return_value = 2048
    mock_read_excel.side_effect = KeyError("Missing column")

    result = read_transactions_from_excel("invalid.xlsx")

    assert result == []


@patch("src.file_readers.os.path.exists")
@patch("src.file_readers.os.path.getsize")
@patch("src.file_readers.pd.read_excel")
def test_read_excel_empty_result(
    mock_read_excel: MagicMock,
    mock_getsize: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Тест: Excel с пустым результатом."""
    mock_exists.return_value = True
    mock_getsize.return_value = 2048

    mock_df = MagicMock()
    mock_df.to_dict.return_value = []
    mock_read_excel.return_value = mock_df

    result = read_transactions_from_excel("data/empty.xlsx")

    assert result == []