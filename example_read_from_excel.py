from src.file_readers import read_transactions_from_excel


def main() -> None:
    """Демонстрация чтения транзакций из Excel."""

    print("=" * 70)
    print("ЧТЕНИЕ ТРАНЗАКЦИЙ ИЗ EXCEL-ФАЙЛА")
    print("=" * 70)

    # Путь к Excel-файлу
    excel_path = "data/transactions_excel.xlsx"

    # Чтение транзакций из Excel
    excel_transactions = read_transactions_from_excel(excel_path)

    if excel_transactions:
        print(f"\n✅ Найдено {len(excel_transactions)} транзакций в Excel:\n")

        for i, transaction in enumerate(excel_transactions[:5], 1):  # Первые 3
            print(f"Транзакция #{i}:")
            print(f"  ID:          {transaction.get('id')}")
            print(f"  Сумма:       {transaction.get('amount')} {transaction.get('currency_code')}")
            print(f"  Описание:    {transaction.get('description')}")
            print()
    else:
        print("❌ Транзакции не найдены или файл пуст.")


if __name__ == "__main__":
    main()
