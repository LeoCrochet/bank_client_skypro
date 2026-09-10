from src.file_readers import read_transactions_from_csv


def main() -> None:
    """Демонстрация чтения транзакций из CSV и Excel."""

    print("=" * 70)
    print("ЧТЕНИЕ ТРАНЗАКЦИЙ ИЗ CSV-ФАЙЛА")
    print("=" * 70)

    # Путь к CSV-файлу
    csv_path = "data/transactions.csv"

    # Чтение транзакций из CSV
    csv_transactions = read_transactions_from_csv(csv_path)

    if csv_transactions:
        print(f"\n✅ Найдено {len(csv_transactions)} транзакций в CSV:\n")

        for i, transaction in enumerate(csv_transactions, 1):
            print(f"Транзакция #{i}:")
            print(f"  ID:          {transaction.get('id')}")
            print(f"  Статус:      {transaction.get('state')}")
            print(f"  Дата:        {transaction.get('date')}")
            print(f"  Сумма:       {transaction.get('amount')} {transaction.get('currency_code')}")
            print(f"  Валюта:      {transaction.get('currency_name')}")
            print(f"  Откуда:      {transaction.get('from')}")
            print(f"  Куда:        {transaction.get('to')}")
            print(f"  Описание:    {transaction.get('description')}")
            print()
    else:
        print("❌ Транзакции не найдены или файл пуст.")

    print("=" * 70)
    print("ЧТЕНИЕ ТРАНЗАКЦИЙ ИЗ EXCEL-ФАЙЛА")
    print("=" * 70)


if __name__ == "__main__":
    main()
