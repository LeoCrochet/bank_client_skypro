"""Пример использования функций маскировки."""

from src.masks import get_mask_account, get_mask_card_number

# Примеры для карт
card_numbers = [
    "1234567890123456",
    "1111222233334444",
    "9876543210987654",
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

from src.widget import  mask_account_card


print("=" * 50)
print("Демонстрация работы функции mask_account_card:")
print("=" * 50)

examples = [
        "Visa Platinum 7000792289606365",
        "Maestro 7000792289606361",
        "MasterCard 1234567890123456",
        "Счет 73654108430135874305",
        "счет 1234567897890",
    ]

for example in examples:
    result = mask_account_card(example)
    print(f"{example:40} -> {result}")

print("\n" + "=" * 50)
print("Демонстрация работы функции get_date:")
print("=" * 50)


