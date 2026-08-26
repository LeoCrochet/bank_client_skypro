"""Модуль для маскировки номеров банковских карт и счетов."""
import logging, os
# Настройка логгера для модуля masks
logger = logging.getLogger('masks')
logger.setLevel(logging.INFO)

# Создаем директорию logs, если её нет
os.makedirs('logs', exist_ok=True)

# Очищаем файл лога при запуске (перезапись)
if os.path.exists('logs/masks.log'):
    with open('logs/masks.log', 'w') as f:
        pass

# Настройка обработчика для записи в файл
file_handler = logging.FileHandler('logs/masks.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Формат лога: время | модуль | уровень | сообщение
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Формат: XXXX XX** **** XXXX
    Пример: 1234 56** **** 1234

    Args:
        card_number (str): Номер карты в виде строки (16 цифр)

    Returns:
        str: Замаскированный номер карты

    Raises:
        ValueError: Если номер карты содержит не 16 цифр
    """
    # Удаляем все пробелы и проверяем длину
    try:
        logger.info(
            f"Начало маскировки карты: {card_number[:4] if len(card_number) >= 4
            else card_number}****{card_number[-4:] if len(card_number) >= 4 
            else ''}")

        # Удаляем все пробелы и проверяем длину
        clean_number = card_number.replace("\t", "").replace(" ", "")

        if not clean_number.isdigit():
            logger.error(f"Номер карты содержит нецифровые символы: {card_number}")
            raise ValueError("Номер карты должен содержать только цифры")

        if len(clean_number) != 16:
            logger.error(f"Неверная длина номера карты: {len(clean_number)} (ожидается 16)")
            raise ValueError("Номер карты должен содержать 16 цифр")

        # Маскируем номер: первые 6 цифр, затем **, затем последние 4 цифры
        masked = f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"

        logger.info(f"Успешная маскировка карты: {masked}")
        return masked

    except ValueError as e:
        logger.error(f"Ошибка при маскировке карты: {e}")
        raise


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    Формат: **XXXX
    Пример: **1234

    Args:
        account_number (str): Номер счета в виде строки

    Returns:
        str: Замаскированный номер счета (только последние 4 цифры)

    Raises:
        ValueError: Если номер счета содержит менее 4 цифр
    """
    # Удаляем все пробелы
    try:
        logger.info(
            f"Начало маскировки счета: {account_number[:2] if len(account_number) >= 2
            else account_number}****{account_number[-4:] if len(account_number) >= 4
            else ''}")

        # Удаляем все пробелы
        clean_number = account_number.replace(" ", "").replace("\t", "")

        if len(clean_number) < 4:
            logger.error(f"Неверная длина номера счета: {len(clean_number)} (минимум 4)")
            raise ValueError("Номер счета должен содержать минимум 4 цифры")

        if not clean_number.isdigit():
            logger.error(f"Номер счета содержит нецифровые символы: {account_number}")
            raise ValueError("Номер счета должен содержать только цифры")

        # Показываем только последние 4 цифры, остальное маскируем
        masked = f"**{clean_number[-4:]}"

        logger.info(f"Успешная маскировка счета: {masked}")
        return masked

    except ValueError as e:
        logger.error(f"Ошибка при маскировке счета: {e}")
        raise
