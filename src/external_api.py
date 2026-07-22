import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv


load_dotenv(".env")
API_KEY = os.getenv("API_KEY_EXCHANGER")


def convert_amount_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли (RUB).

    Если валюта транзакции 'RUB', возвращает исходную сумму.
    Если валюта 'USD' или 'EUR', получает текущий курс через внешнее API.
    В случае ошибки API или неизвестной валюты, возвращает 0.0.
    """
    try:
        operation_amount = transaction.get("operationAmount", {})
        amount_str = operation_amount.get("amount")
        currency_code = operation_amount.get("currency", {}).get("code")

        if amount_str is None or currency_code is None:
            print(f"Ошибка: не найдена сумма или валюта в транзакции: {transaction}")
            return 0.0

        amount = float(amount_str)

        if currency_code == "RUB":
            return amount

        if currency_code not in ("USD", "EUR"):
            print(f"Ошибка: валюта '{currency_code}' не поддерживается для конвертации.")
            return 0.0

        # Получение курса через API (блок try-except для обработки ошибок сети/API)
        try:
            response = requests.request(
                "GET",
                f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount={amount}",
                headers={"apikey": API_KEY},
            )
            response.raise_for_status()  # Вызовет исключение для статусов 4xx/5xx

            data = response.json()

            return data.get("result", 0.0)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к API для валюты {currency_code}: {e}")
            return 0.0

    except (ValueError, TypeError, KeyError) as e:
        print(f"Ошибка при разборе данных транзакции: {e}")
        return 0.0
