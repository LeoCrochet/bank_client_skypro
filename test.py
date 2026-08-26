from src.utils import get_transactions_from_json


print("-" * 50)
print("\n6. ЧТЕНИЕ СПИСКА ОПЕРАЦИЙ ИЗ ФАЙЛА data/operations.json")
transactions = get_transactions_from_json("data/operations_test.json")
print(transactions)
print("-" * 50)
