"""Модуль с декораторами для логирования."""

import functools
import logging
import sys
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования выполнения функции."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Настраиваем логгер для функции
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            # Очищаем существующие обработчики
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

            # Создаем новый обработчик
            if filename:
                handler = logging.FileHandler(filename, encoding='utf-8')
            else:
                handler = logging.StreamHandler(sys.stdout)

            handler.setFormatter(logging.Formatter('%(message)s'))
            logger.addHandler(handler)

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result

            except Exception as e:
                # Логируем ошибку
                error_type = type(e).__name__
                args_repr = ", ".join(repr(arg) for arg in args)
                kwargs_repr = f", {kwargs}" if kwargs else ""
                logger.error(f"{func.__name__} error: {error_type}. Inputs: ({args_repr}{kwargs_repr})")
                raise

        return wrapper

    return decorator