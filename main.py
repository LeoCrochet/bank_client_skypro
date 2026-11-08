"""Основной модуль программы для работы с банковскими транзакциями."""

from typing import Any, Dict, List

import pandas as pd

from src.file_readers import read_transactions_from_csv, read_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.search_operations import process_bank_search
from src.utils import get_transactions_from_json
from src.widget import get_date, mask_account_card


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль (поддерживает JSON, CSV, Excel)."""
    date_str = get_date(transaction.get("date", ""))
    description = transaction.get("description", "")

    # Безопасная маскировка (превращаем NaN/None в пустую строку)
    from_acc = transaction.get("from")
    to_acc = transaction.get("to")

    from_str = str(from_acc) if from_acc and not pd.isna(from_acc) else ""
    to_str = str(to_acc) if to_acc and not pd.isna(to_acc) else ""

    masked_from = mask_account_card(from_str) if from_str else ""
    masked_to = mask_account_card(to_str) if to_str else ""

    # Формирование строки перевода
    if masked_from and masked_to:
        transfer_info = f"{masked_from} -> {masked_to}"
    elif masked_from:
        transfer_info = masked_from
    elif masked_to:
        transfer_info = masked_to
    else:
        transfer_info = ""

    # Информация о сумме (поддержка JSON и CSV/Excel)
    amount_info = transaction.get("operationAmount", {})

    if amount_info and isinstance(amount_info, dict):
        # Для JSON
        amount_val = amount_info.get("amount", "0")
        currency = amount_info.get("currency", {}).get("code", "RUB")
        amount_str = f"Сумма: {amount_val} {currency}"
    else:
        # Для CSV и Excel
        amount_val = transaction.get("amount", "0")
        # Убираем .0 у чисел (например, 34316.0 -> 34316)
        if isinstance(amount_val, float) and amount_val.is_integer():
            amount_val = int(amount_val)

        currency = transaction.get("currency_code", "RUB")
        amount_str = f"Сумма: {amount_val} {currency}"

    return f"{date_str} {description}\n{transfer_info}\n{amount_str}"


def get_user_choice(prompt: str, valid_choices: List[str], default: str | None = None) -> str:
    """Запрашивает у пользователя ввод до тех пор, пока не будет корректного."""
    valid_lower = [c.lower() for c in valid_choices]

    while True:
        user_input = input(prompt).strip()

        if not user_input and default is not None:
            return default.lower()

        if user_input.lower() in valid_lower:
            return user_input.lower()

        print(f"Ошибка ввода. Пожалуйста, выберите из списка: {', '.join(valid_choices)}")


def load_transactions() -> List[Dict[str, Any]]:
    """Запрашивает источник данных и загружает транзакции."""
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = get_user_choice("Пользователь: ", ["1", "2", "3"])

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        return get_transactions_from_json("data/operations.json")
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        return read_transactions_from_csv("data/transactions.csv")
    else:
        print("Программа: Для обработки выбран XLSX-файл.")
        return read_transactions_from_excel("data/transactions_excel.xlsx")


def filter_by_status_interactive(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Запрашивает статус и фильтрует транзакции."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
    print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")

    status = get_user_choice("Пользователь: ", valid_statuses).upper()
    print(f'Программа: Операции отфильтрованы по статусу "{status}"')

    return filter_by_state(transactions, status)


def sort_transactions_interactive(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Спрашивает, нужно ли сортировать, и сортирует."""
    sort_choice = get_user_choice(
        "\nОтсортировать операции по дате? Да/Нет (по умолчанию: Нет): ", ["да", "нет"], default="нет"
    )

    if sort_choice == "да":
        order_choice = get_user_choice(
            "Отсортировать по возрастанию или по убыванию? (по возрастанию/по убыванию, по умолчанию: по убыванию): ",
            ["по возрастанию", "по убыванию"],
            default="по убыванию",
        )
        descending = order_choice == "по убыванию"
        return sort_by_date(transactions, descending=descending)
    return transactions


def filter_rub_interactive(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Спрашивает, нужно ли фильтровать по рублям, и фильтрует."""
    rub_choice = get_user_choice(
        "\nВыводить только рублевые транзакции? Да/Нет (по умолчанию: Нет): ", ["да", "нет"], default="нет"
    )

    if rub_choice == "да":
        rub_transactions = []
        for t in transactions:
            op_amount = t.get("operationAmount", {})
            if op_amount and op_amount.get("currency", {}).get("code") == "RUB":
                rub_transactions.append(t)
            elif t.get("currency_code") == "RUB":
                rub_transactions.append(t)
        return rub_transactions
    return transactions


def search_interactive(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Спрашивает, нужен ли поиск, и выполняет его."""
    search_choice = get_user_choice(
        "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет (по умолчанию: Нет): ",
        ["да", "нет"],
        default="нет",
    )

    if search_choice == "да":
        search_word = input("Введите слово для поиска: ").strip()
        return process_bank_search(transactions, search_word)
    return transactions


def main() -> None:
    """Основная логика программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # 1. Загрузка
    transactions = load_transactions()
    if not transactions:
        print("Не удалось загрузить данные или файл пуст.")
        return

    # 2. Фильтрация по статусу
    try:
        filtered_transactions = filter_by_status_interactive(transactions)
    except ValueError:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 3. Сортировка
    filtered_transactions = sort_transactions_interactive(filtered_transactions)

    # 4. Фильтрация по рублям
    filtered_transactions = filter_rub_interactive(filtered_transactions)

    # 5. Поиск по описанию
    filtered_transactions = search_interactive(filtered_transactions)

    # 6. Вывод
    print("\nРаспечатываю итоговый список транзакций...")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    for t in filtered_transactions:
        print(format_transaction(t))
        print("-" * 40)


if __name__ == "__main__":
    main()
