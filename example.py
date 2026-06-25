# Новая ветка develop
"""Пример использования функций маскировки."""

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
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
