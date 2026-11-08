"""Основной модуль программы для работы с банковскими транзакциями."""

from typing import Any, Dict, List

from src.external_api import convert_amount_to_rub
from src.file_readers import read_transactions_from_csv, read_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.search_operations import process_bank_search
from src.utils import get_transactions_from_json
from src.widget import get_date, mask_account_card


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль."""
    date_str = get_date(transaction.get("date", ""))
    description = transaction.get("description", "")

    # Маскировка отправителя и получателя
    from_acc = transaction.get("from", "")
    to_acc = transaction.get("to", "")

    masked_from = mask_account_card(from_acc) if from_acc else ""
    masked_to = mask_account_card(to_acc) if to_acc else ""

    # Формирование строки перевода
    if masked_from and masked_to:
        transfer_info = f"{masked_from} -> {masked_to}"
    elif masked_from:
        transfer_info = masked_from
    elif masked_to:
        transfer_info = masked_to
    else:
        transfer_info = ""

    # Информация о сумме
    amount_info = transaction.get("operationAmount", {})
    if amount_info:
        amount_val = amount_info.get("amount", "0")
        currency = amount_info.get("currency", {}).get("code", "RUB")
        amount_str = f"Сумма: {amount_val} {currency}"
    else:
        try:
            amount_rub = convert_amount_to_rub(transaction)
            amount_str = f"Сумма: {int(amount_rub)} руб."
        except Exception:
            amount_str = "Сумма: 0 руб."

    # Сборка итоговой строки
    return f"{date_str} {description}\n{transfer_info}\n{amount_str}"


def get_user_choice(
    prompt: str,
    valid_choices: List[str],
    default: str | None = None
) -> str:
    """
    Запрашивает у пользователя ввод до тех пор, пока не будет корректного.

    Если пользователь нажимает Enter и передан параметр default, возвращается default.
    """
    valid_lower = [c.lower() for c in valid_choices]

    while True:
        user_input = input(prompt).strip()

        # Если введена пустая строка и есть значение по умолчанию
        if not user_input and default is not None:
            return default.lower()

        if user_input.lower() in valid_lower:
            return user_input.lower()

        print(f"Ошибка ввода. Пожалуйста, выберите из списка: {', '.join(valid_choices)}")


def main() -> None:
    """Основная логика программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # 1. Выбор источника данных
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = get_user_choice("Пользователь: ", ["1", "2", "3"])

    transactions: List[Dict[str, Any]] = []

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        transactions = get_transactions_from_json("data/operations.json")
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        transactions = read_transactions_from_csv("data/transactions.csv")
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        transactions = read_transactions_from_excel("data/transactions_excel.xlsx")

    if not transactions:
        print("Не удалось загрузить данные или файл пуст.")
        return

    # 2. Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
    print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")

    status = get_user_choice("Пользователь: ", valid_statuses).upper()
    print(f"Программа: Операции отфильтрованы по статусу \"{status}\"")

    try:
        filtered_transactions = filter_by_state(transactions, status)
    except ValueError:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 3. Сортировка по дате (по умолчанию - Нет)
    sort_choice = get_user_choice(
        "\nОтсортировать операции по дате? Да/Нет (по умолчанию: Нет): ",
        ["да", "нет"],
        default="нет"
    )

    if sort_choice == "да":
        order_choice = get_user_choice(
            "Отсортировать по возрастанию или по убыванию? (по возрастанию/по убыванию, по умолчанию: по убыванию): ",
            ["по возрастанию", "по убыванию"],
            default="по убыванию"
        )
        descending = order_choice == "по убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, descending=descending)

    # 4. Фильтрация по рублям (по умолчанию - Нет)
    rub_choice = get_user_choice(
        "\nВыводить только рублевые транзакции? Да/Нет (по умолчанию: Нет): ",
        ["да", "нет"],
        default="нет"
    )

    if rub_choice == "да":
        rub_transactions = []
        for t in filtered_transactions:
            op_amount = t.get("operationAmount", {})
            if op_amount and op_amount.get("currency", {}).get("code") == "RUB":
                rub_transactions.append(t)
            elif t.get("currency_code") == "RUB":
                rub_transactions.append(t)
        filtered_transactions = rub_transactions

    # 5. Поиск по слову (по умолчанию - Нет)
    search_choice = get_user_choice(
        "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет (по умолчанию: Нет): ",
        ["да", "нет"],
        default="нет"
    )

    if search_choice == "да":
        search_word = input("Введите слово для поиска: ").strip()
        filtered_transactions = process_bank_search(filtered_transactions, search_word)

    # 6. Вывод результата
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