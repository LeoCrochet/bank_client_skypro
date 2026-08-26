"""Тесты для модуля utils."""

import json
import os
import tempfile
from typing import Generator

import pytest

from src.utils import get_transactions_from_json


@pytest.fixture
def temp_json_file() -> Generator[str, None, None]:
    """Фикстура: создает временный JSON-файл и удаляет его после теста."""
    fd, filename = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield filename
    if os.path.exists(filename):
        os.unlink(filename)


def test_get_transactions_from_json_valid(temp_json_file: str) -> None:
    """Тест: чтение валидного JSON-файла со списком транзакций."""
    test_data = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"},
    ]

    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    result = get_transactions_from_json(temp_json_file)

    assert result == test_data
    assert len(result) == 2


def test_get_transactions_from_json_empty_file(temp_json_file: str) -> None:
    """Тест: пустой файл."""
    # Создаем пустой файл
    with open(temp_json_file, "w", encoding="utf-8"):
        pass

    result = get_transactions_from_json(temp_json_file)

    assert result == []


def test_get_transactions_from_json_not_found() -> None:
    """Тест: файл не найден."""
    result = get_transactions_from_json("non_existent_file.json")

    assert result == []


def test_get_transactions_from_json_invalid_json(temp_json_file: str) -> None:
    """Тест: невалидный JSON."""
    with open(temp_json_file, "w", encoding="utf-8") as f:
        f.write("{invalid json}")

    result = get_transactions_from_json(temp_json_file)

    assert result == []


def test_get_transactions_from_json_not_list(temp_json_file: str) -> None:
    """Тест: JSON не является списком."""
    test_data = {"key": "value"}

    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    result = get_transactions_from_json(temp_json_file)

    assert result == []


def test_get_transactions_from_json_empty_list(temp_json_file: str) -> None:
    """Тест: пустой список в JSON."""
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump([], f)

    result = get_transactions_from_json(temp_json_file)

    assert result == []


def test_get_transactions_from_json_real_file() -> None:
    """Тест: чтение реального файла operations.json."""
    result = get_transactions_from_json("data/operations.json")

    # Проверяем, что файл существует и содержит данные
    if os.path.exists("data/operations.json"):
        assert isinstance(result, list)
        if result:
            assert "id" in result[0]
            assert "state" in result[0]
            assert "date" in result[0]
    else:
        # Если файла нет, функция должна вернуть пустой список
        assert result == []
