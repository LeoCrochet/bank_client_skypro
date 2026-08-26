"""Тесты для модуля external_api."""

from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.external_api import convert_amount_to_rub


# -------- ТЕСТОВЫЕ ДАННЫЕ --------


@pytest.fixture
def rub_transaction() -> Dict[str, Any]:
    """Фикстура: транзакция в рублях."""
    return {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "RUB", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    }


@pytest.fixture
def usd_transaction() -> Dict[str, Any]:
    """Фикстура: транзакция в долларах."""
    return {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }


@pytest.fixture
def eur_transaction() -> Dict[str, Any]:
    """Фикстура: транзакция в евро."""
    return {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "EUR", "code": "EUR"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    }


@pytest.fixture
def btc_transaction() -> Dict[str, Any]:
    """Фикстура: транзакция в биткоинах (неподдерживаемая валюта)."""
    return {
        "id": 123456789,
        "state": "EXECUTED",
        "date": "2024-01-01T12:00:00.000000",
        "operationAmount": {"amount": "1000.00", "currency": {"name": "BTC", "code": "BTC"}},
        "description": "Покупка криптовалюты",
        "from": "Счет 12345678901234567890",
        "to": "Кошелек 1A2B3C4D5E6F7G8H9I0J",
    }


@pytest.fixture
def invalid_transaction() -> Dict[str, Any]:
    """Фикстура: транзакция без суммы и валюты."""
    return {
        "id": 999999999,
        "state": "EXECUTED",
        "date": "2024-01-01T12:00:00.000000",
        "description": "Невалидная транзакция",
    }


# -------- ТЕСТЫ ДЛЯ RUB (БЕЗ API) --------


def test_convert_rub_transaction(rub_transaction: Dict[str, Any]) -> None:
    """Тест: конвертация рублевой транзакции."""
    result = convert_amount_to_rub(rub_transaction)
    assert result == 43318.34
    assert isinstance(result, float)


def test_convert_rub_transaction_returns_float() -> None:
    """Тест: возвращается float для RUB."""
    transaction = {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}}
    result = convert_amount_to_rub(transaction)
    assert result == 100.50
    assert isinstance(result, float)


# -------- ТЕСТЫ ДЛЯ USD (С МОКОМ) --------


@patch("src.external_api.requests.request")
def test_convert_usd_transaction_success(mock_request: MagicMock, usd_transaction: Dict[str, Any]) -> None:
    """Тест: успешная конвертация USD в RUB."""
    # Настраиваем мок ответа API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 869430.195}
    mock_response.raise_for_status = MagicMock()
    mock_request.return_value = mock_response

    result = convert_amount_to_rub(usd_transaction)

    assert result == pytest.approx(869430.195, 0.001)
    assert isinstance(result, float)

    # Проверяем вызов API
    mock_request.assert_called_once()
    call_args = mock_request.call_args
    assert call_args[0][0] == "GET"
    assert "exchangerates_data/convert" in call_args[0][1]
    assert "to=RUB" in call_args[0][1]
    assert "from=USD" in call_args[0][1]
    assert "amount=9824.07" in call_args[0][1]
    assert call_args[1]["headers"]["apikey"] is not None


@patch("src.external_api.requests.request")
def test_convert_usd_transaction_api_error(mock_request: MagicMock, usd_transaction: Dict[str, Any]) -> None:
    """Тест: ошибка API при конвертации USD."""
    mock_request.side_effect = requests.exceptions.RequestException("API connection error")

    result = convert_amount_to_rub(usd_transaction)

    assert result == 0.0


@patch("src.external_api.requests.request")
def test_convert_usd_transaction_http_error(mock_request: MagicMock, usd_transaction: Dict[str, Any]) -> None:
    """Тест: HTTP ошибка при запросе к API."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("HTTP 404")
    mock_request.return_value = mock_response

    result = convert_amount_to_rub(usd_transaction)

    assert result == 0.0


@patch("src.external_api.requests.request")
def test_convert_usd_transaction_missing_result(mock_request: MagicMock, usd_transaction: Dict[str, Any]) -> None:
    """Тест: отсутствие 'result' в ответе API."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_response.raise_for_status = MagicMock()
    mock_request.return_value = mock_response

    result = convert_amount_to_rub(usd_transaction)

    assert result == 0.0


@patch("src.external_api.requests.request")
def test_convert_usd_transaction_empty_response(mock_request: MagicMock, usd_transaction: Dict[str, Any]) -> None:
    """Тест: пустой ответ от API."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 0.0}
    mock_response.raise_for_status = MagicMock()
    mock_request.return_value = mock_response

    result = convert_amount_to_rub(usd_transaction)

    assert result == 0.0


# -------- ТЕСТЫ ДЛЯ EUR (С МОКОМ) --------


@patch("src.external_api.requests.request")
def test_convert_eur_transaction_success(mock_request: MagicMock, eur_transaction: Dict[str, Any]) -> None:
    """Тест: успешная конвертация EUR в RUB."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7530739.336}
    mock_response.raise_for_status = MagicMock()
    mock_request.return_value = mock_response

    result = convert_amount_to_rub(eur_transaction)

    assert result == pytest.approx(7530739.336, 0.001)
    assert isinstance(result, float)

    mock_request.assert_called_once()
    call_args = mock_request.call_args
    assert "from=EUR" in call_args[0][1]
    assert "amount=79114.93" in call_args[0][1]


@patch("src.external_api.requests.request")
def test_convert_eur_transaction_api_error(mock_request: MagicMock, eur_transaction: Dict[str, Any]) -> None:
    """Тест: ошибка API при конвертации EUR."""
    mock_request.side_effect = requests.exceptions.RequestException("API timeout")

    result = convert_amount_to_rub(eur_transaction)

    assert result == 0.0


# -------- ТЕСТЫ ДЛЯ НЕПОДДЕРЖИВАЕМЫХ ВАЛЮТ --------


def test_convert_btc_transaction(btc_transaction: Dict[str, Any]) -> None:
    """Тест: конвертация неподдерживаемой валюты (BTC)."""
    result = convert_amount_to_rub(btc_transaction)
    assert result == 0.0


# -------- ТЕСТЫ ДЛЯ НЕВАЛИДНЫХ ТРАНЗАКЦИЙ --------


def test_convert_invalid_transaction(invalid_transaction: Dict[str, Any]) -> None:
    """Тест: транзакция без суммы и валюты."""
    result = convert_amount_to_rub(invalid_transaction)
    assert result == 0.0


def test_convert_empty_transaction() -> None:
    """Тест: пустая транзакция."""
    result = convert_amount_to_rub({})
    assert result == 0.0


def test_convert_transaction_without_currency() -> None:
    """Тест: транзакция без валюты."""
    transaction = {"operationAmount": {"amount": "1000.00"}}
    result = convert_amount_to_rub(transaction)
    assert result == 0.0


def test_convert_transaction_without_amount() -> None:
    """Тест: транзакция без суммы."""
    transaction = {"operationAmount": {"currency": {"code": "USD"}}}
    result = convert_amount_to_rub(transaction)
    assert result == 0.0


# -------- ТЕСТЫ НА ТИПЫ --------


@patch("src.external_api.requests.request")
def test_convert_usd_handles_string_amount(mock_request: MagicMock, usd_transaction: Dict[str, Any]) -> None:
    """Тест: сумма транзакции может быть строкой."""
    usd_transaction["operationAmount"]["amount"] = "1000.50"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 88544.25}
    mock_response.raise_for_status = MagicMock()
    mock_request.return_value = mock_response

    result = convert_amount_to_rub(usd_transaction)

    assert result == pytest.approx(88544.25, 0.001)


@patch("src.external_api.requests.request")
def test_convert_usd_handles_float_amount(mock_request: MagicMock, usd_transaction: Dict[str, Any]) -> None:
    """Тест: сумма транзакции может быть float."""
    usd_transaction["operationAmount"]["amount"] = 1000.50

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 88544.25}
    mock_response.raise_for_status = MagicMock()
    mock_request.return_value = mock_response

    result = convert_amount_to_rub(usd_transaction)

    assert result == pytest.approx(88544.25, 0.001)


# -------- ТЕСТЫ НА МНОЖЕСТВЕННЫЕ ВЫЗОВЫ --------


@patch("src.external_api.requests.request")
def test_convert_multiple_transactions(
    mock_request: MagicMock, usd_transaction: Dict[str, Any], eur_transaction: Dict[str, Any]
) -> None:
    """Тест: несколько транзакций с разными валютами."""
    # Настраиваем мок на последовательные ответы
    mock_response1 = MagicMock()
    mock_response1.status_code = 200
    mock_response1.json.return_value = {"result": 869430.195}
    mock_response1.raise_for_status = MagicMock()

    mock_response2 = MagicMock()
    mock_response2.status_code = 200
    mock_response2.json.return_value = {"result": 7530739.336}
    mock_response2.raise_for_status = MagicMock()

    mock_request.side_effect = [mock_response1, mock_response2]

    result_usd = convert_amount_to_rub(usd_transaction)
    result_eur = convert_amount_to_rub(eur_transaction)

    assert result_usd == pytest.approx(869430.195, 0.001)
    assert result_eur == pytest.approx(7530739.336, 0.001)
    assert mock_request.call_count == 2
