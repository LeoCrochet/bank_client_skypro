from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в строке.

    Функция принимает строку с типом и номером карты/счета и возвращает
    строку с замаскированным номером. Разделение строки на имя и номер
    происходит внутри функции, но пользователь передает только один аргумент.

    Args:
        account_info (str): Строка с типом и номером.
            Примеры: "Visa Platinum 7000792289606361"
                    "Maestro 7000792289606361"
                    "Счет 73654108430135874305"

    Raises:
        ValueError: Если не удалось определить тип карты/счета

    Returns:
        str: Строка с замаскированным номером.
            Примеры: "Visa Platinum 7000 79** **** 6361"
                    "Счет **4305"
    """
    parts = account_info.rsplit(" ", 1)

    if len(parts) != 2:
        raise ValueError(f"Некорректный формат строки: {account_info}")

    card_type, number = parts[0], parts[1]

    # Определяем тип и применяем соответствующую маскировку
    if "Счет" in card_type or "счет" in card_type:
        # Для счета используем маскировку счета
        masked_number = get_mask_account(number)
    else:
        # Для карты используем маскировку карты
        masked_number = get_mask_card_number(number)

    return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует строку с датой из формата ISO в формат ДД.ММ.ГГГГ.
    Использует datetime

    Args:
        date_string (str): Строка с датой в формате "YYYY-MM-DDTHH:MM:SS.ms"

    Returns:
        str: Дата в формате "ДД.ММ.ГГГГ"
    """
    try:

        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%d.%m.%Y")

    except ValueError:

        try:
            # Пробуем парсить только дату (без времени)
            dt = datetime.strptime(date_string[:10], "%Y-%m-%d")
            return dt.strftime("%d.%m.%Y")
        except (ValueError, IndexError) as e:
            raise ValueError(f"Некорректный формат даты: {date_string}. Ожидается ISO формат") from e
