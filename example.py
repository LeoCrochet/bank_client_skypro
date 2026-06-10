#Новая ветка develop
"""Пример использования функций маскировки."""

from src.masks import get_mask_account, get_mask_card_number
from src.widget import get_date, mask_account_card


# Примеры для карт
card_numbers = [
    "1234567890123456",
    "1111222233334444",
    "9876543210987654"
]

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
