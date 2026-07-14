import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions() -> list[dict]:
    """Фикстура: список транзакций для тестирования."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
    ]


"""ТЕСТЫ filter_by_currency"""


def test_filter_by_currency(transactions):
    """Тест: фильтрация транзакций по валюте USD."""
    usd_transactions = list(filter_by_currency(transactions, "USD"))

    assert len(usd_transactions) == 3
    assert usd_transactions[0]["id"] == 939719570
    assert usd_transactions[1]["id"] == 142264268


def test_filter_by_currency_no_matches(transactions):
    """Тест: фильтрация по валюте, которой нет в транзакциях."""
    result = list(filter_by_currency(transactions, "EUR"))

    assert len(result) == 0


def test_filter_by_currency_iterator(transactions):
    """Тест: проверка работы итератора."""
    usd_transactions = filter_by_currency(transactions, "USD")

    first = next(usd_transactions)
    assert first["id"] == 939719570

    second = next(usd_transactions)
    assert second["id"] == 142264268


"""ТЕСТЫ transaction_descriptions"""


def test_transaction_descriptions(transactions):
    """Тест: генератор описаний транзакций."""
    descriptions = transaction_descriptions(transactions)

    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    assert next(descriptions) == "Перевод организации"


def test_transaction_descriptions_empty():
    """Тест: генератор с пустым списком."""
    descriptions = transaction_descriptions([])

    with pytest.raises(StopIteration):
        next(descriptions)


def test_transaction_descriptions_missing_description():
    """Тест: транзакция без описания."""
    # Создаем транзакцию без ключа 'description'
    transactions_without_desc = [
        {"id": 1, "description": "Оплата"},
        {"id": 2},  # без description
        {"id": 3, "description": "Перевод"},
    ]

    descriptions = transaction_descriptions(transactions_without_desc)

    assert next(descriptions) == "Оплата"
    assert next(descriptions) == ""  # Пустая строка для отсутствующего описания
    assert next(descriptions) == "Перевод"

    """ТЕСТЫ card_number_generator"""


def test_card_number_generator_range():
    """Тест: генерация номеров карт в диапазоне."""
    result = list(card_number_generator(1, 5))

    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]

    assert result == expected


def test_card_number_generator_large_numbers():
    """Тест: генерация номеров с большими числами."""
    result = list(card_number_generator(9999999999999990, 9999999999999995))

    expected = [
        "9999 9999 9999 9990",
        "9999 9999 9999 9991",
        "9999 9999 9999 9992",
        "9999 9999 9999 9993",
        "9999 9999 9999 9994",
        "9999 9999 9999 9995",
    ]

    assert result == expected


def test_card_number_generator_single_number():
    """Тест: генерация одного номера."""
    result = list(card_number_generator(1234567890123456, 1234567890123456))

    assert result == ["1234 5678 9012 3456"]


def test_card_number_generator_start_less_than_1():
    """Тест: начальное значение меньше 1."""
    with pytest.raises(ValueError, match="Некорректный диапазон"):
        list(card_number_generator(0, 5))


def test_card_number_generator_end_greater_than_max():
    """Тест: конечное значение больше максимального."""
    with pytest.raises(ValueError, match="Некорректный диапазон"):
        list(card_number_generator(1, 10000000000000000))


def test_card_number_generator_start_greater_than_end():
    """Тест: начальное значение больше конечного."""
    with pytest.raises(ValueError, match="Некорректный диапазон"):
        list(card_number_generator(10, 5))


def test_card_number_generator_iterator():
    """Тест: проверка работы итератора."""
    generator = card_number_generator(1, 3)

    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    assert next(generator) == "0000 0000 0000 0003"

    with pytest.raises(StopIteration):
        next(generator)
