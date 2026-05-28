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

    Returns:
        str: Строка с замаскированным номером.
            Примеры: "Visa Platinum 7000 79** **** 6361"
                    "Счет **4305"
    """
    parts = account_info.rsplit(" ", 1)

    card_type, number = parts[0], parts[1]

# Определяем тип и применяем соответствующую маскировку
    if "Счет" in card_type or "счет" in card_type:
        # Для счета используем маскировку счета
        masked_number = get_mask_account(number)
    else:
        # Для карты используем маскировку карты

        masked_number = get_mask_card_number(number)

    return f"{card_type} {masked_number}"