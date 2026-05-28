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