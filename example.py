"""примеры использования функций модулей masks.py, processing.py, widget.py, generators.py"""

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.utils import get_transactions_from_json
from src.widget import get_date, mask_account_card


# Примеры для карт
card_numbers = ["1234567890123456", "1111222233334444", "9876543210987654"]

print("Маскировка номеров карт:")
for card in card_numbers:
    masked = get_mask_card_number(card)
    print(f"{card} -> {masked}")

print("\nМаскировка номеров счетов:")
# Примеры для счетов
account_numbers = [
    "1234567890",
    "9876543210",
    "11111111111111111111",
]

for account in account_numbers:
    masked = get_mask_account(account)
    print(f"{account} -> {masked}")


print("=" * 50)
print("Демонстрация работы функции mask_account_card:")
print("=" * 50)

examples = [
    "Visa Platinum 7000792289606365",
    "Maestro 7000792289606361",
    "MasterCard 1234567890123456",
    "Счет 73654108430185874305",
    "счет 12333",
]


for example in examples:
    result = mask_account_card(example)
    print(f"{example:40} -> {result}")

print("\n" + "=" * 50)
print("Демонстрация работы функции get_date:")
print("=" * 50)

dates = [
    "2024-03-11T02:26:18.671407",
    "2023-12-25T15:30:00.000000",
    "2024-01-01",
    "2024-02-29T10:30:45.123456",
]

for date_string in dates:
    result = get_date(date_string)
    print(f"{date_string:35} -> {result}")

"""Демонстрация фильтрации транзакций."""

# Исходные данные
transactions = [
    {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]
print("\n" * 2 + "=" * 70)
print("Демонстрация фильтрации транзакций.".upper())
print("=" * 70)
print("=" * 70)
print("ИСХОДНЫЙ СПИСОК ТРАНЗАКЦИЙ:")
print("=" * 70)
for transaction in transactions:
    print(f"  {transaction}")

print("=" * 70)
print("ФИЛЬТРАЦИЯ ПО СТАТУСУ 'EXECUTED' (по умолчанию):")
print("=" * 70)
executed = filter_by_state(transactions)
for transaction in executed:
    print(f"  {transaction}")

print("=" * 70)
print("ФИЛЬТРАЦИЯ ПО СТАТУСУ 'CANCELED':")
print("=" * 70)
canceled = filter_by_state(transactions, "CANCELED")
for transaction in canceled:
    print(f"  {transaction}")

"""Демонстрация сортировки транзакций."""
print("\n" * 2 + "=" * 70)
print("Демонстрация сортировки транзакций.".upper())
print("=" * 70)
print("=" * 70)
print("СОРТИРОВКА ПО УБЫВАНИЮ (НОВЫЕ СВЕРХУ) - ПО УМОЛЧАНИЮ:")
print("=" * 70)

sorted_desc = sort_by_date(transactions)
for transaction in sorted_desc:
    print(f"  {transaction}")

print("=" * 70)
print("СОРТИРОВКА ПО ВОЗРАСТАНИЮ (СТАРЫЕ СВЕРХУ):")
print("=" * 70)

sorted_asc = sort_by_date(transactions, descending=False)
for transaction in sorted_asc:
    print(f"  {transaction}")

# пример использования функций generators.py
transactions = [
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
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
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
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]
print("=" * 70)
print("ДЕМОНСТРАЦИЯ РАБОТЫ ГЕНЕРАТОРОВ")
print("=" * 70)

# -------- 1. filter_by_currency --------
print("\n1. ФИЛЬТРАЦИЯ ПО ВАЛЮТЕ (filter_by_currency):")
print("-" * 50)

usd_transactions = filter_by_currency(transactions, "USD")
print("Транзакции в USD:")
for i in range(3):
    try:
        transaction = next(usd_transactions)
        print(f"  {i + 1}. ID: {transaction['id']}, Сумма: {transaction['operationAmount']['amount']} USD")
    except StopIteration:
        break

    # -------- 2. transaction_descriptions --------
print("\n2. ОПИСАНИЯ ТРАНЗАКЦИЙ (transaction_descriptions):")
print("-" * 50)

descriptions = transaction_descriptions(transactions)
print("Описания транзакций:")
for i in range(5):
    try:
        desc = next(descriptions)
        print(f"  {i + 1}. {desc}")
    except StopIteration:
        break

    # -------- 3. card_number_generator --------
print("\n3. ГЕНЕРАЦИЯ НОМЕРОВ КАРТ (card_number_generator):")
print("-" * 50)

print("Номера карт с 1 по 5:")
for card_number in card_number_generator(1, 5):
    print(f"  {card_number}")

print("\nНомера карт с 9999999999999990 по 9999999999999995:")
for card_number in card_number_generator(9999999999999990, 9999999999999995):
    print(f"  {card_number}")

    # -------- 4. КОМБИНАЦИЯ ГЕНЕРАТОРОВ --------
print("\n4. КОМБИНАЦИЯ ГЕНЕРАТОРОВ:")
print("-" * 50)

print("USD транзакции и их описания:")
usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(f"  ID: {transaction['id']} - {transaction['description']}")

    # -------- 5. ИСПОЛЬЗОВАНИЕ В ЦИКЛАХ --------
print("\n5. ИСПОЛЬЗОВАНИЕ В ЦИКЛАХ:")
print("-" * 50)

print("Первые 3 транзакции в USD:")
for i, transaction in enumerate(filter_by_currency(transactions, "USD")):
    if i >= 3:
        break
    print(f"  {i + 1}. {transaction['description']} - {transaction['operationAmount']['amount']} USD")

    # -------- 6. ПРОВЕРКА НА ОТСУТСТВИЕ ДАННЫХ --------
print("\n6. ФИЛЬТРАЦИЯ ПО ВАЛЮТЕ EUR (нет совпадений):")
print("-" * 50)

eur_transactions = filter_by_currency(transactions, "EUR")
eur_list = list(eur_transactions)
if not eur_list:
    print("  Транзакции в EUR не найдены")

print("-" * 50)
print("\n6. ЧТЕНИЕ СПИСКА ОПЕРАЦИЙ ИЗ ФАЙЛА data/operations.json")
transactions = get_transactions_from_json("data/operations.json")
print(transactions)
print("-" * 50)
