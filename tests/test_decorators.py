"""Тесты для модуля decorators."""

from typing import Any, Generator
import os
import tempfile
import pytest

from src.decorators import log


@pytest.fixture
def temp_file() -> Generator[str, None, None]:
    """Фикстура: создает временный файл и удаляет его после теста."""
    # Создаем временный файл
    fd, filename = tempfile.mkstemp()
    os.close(fd)  # Закрываем дескриптор, чтобы файл можно было использовать

    yield filename

    # Удаляем файл после теста
    if os.path.exists(filename):
        try:
            os.unlink(filename)
        except PermissionError:
            # На Windows может быть задержка, пробуем еще раз
            import time
            time.sleep(0.1)
            try:
                os.unlink(filename)
            except PermissionError:
                pass  # Игнорируем, если не удалось удалить


# -------- ТЕСТЫ ДЛЯ ЛОГИРОВАНИЯ В КОНСОЛЬ --------

def test_log_to_console_success(capsys: Any) -> None:
    """Тест: логирование успешного выполнения в консоль."""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(3, 5)
    assert result == 8

    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_to_console_error(capsys: Any) -> None:
    """Тест: логирование ошибки в консоль."""

    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0)" in captured.out


def test_log_multiple_calls_to_console(capsys: Any) -> None:
    """Тест: несколько вызовов функции с логированием в консоль."""

    @log()
    def increment(x: int) -> int:
        return x + 1

    increment(1)
    increment(2)
    increment(3)

    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    assert len(lines) == 3
    for line in lines:
        assert "increment ok" in line


def test_log_to_file_success(temp_file: str) -> None:
    """Тест: логирование успешного выполнения в файл."""

    @log(filename=temp_file)
    def multiply(a: int, b: int) -> int:
        return a * b

    result = multiply(4, 5)
    assert result == 20

    with open(temp_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "multiply ok" in content


def test_log_to_file_error(temp_file: str) -> None:
    """Тест: логирование ошибки в файл."""

    @log(filename=temp_file)
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    with open(temp_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "divide error: ZeroDivisionError" in content
        assert "Inputs: (10, 0)" in content


def test_log_multiple_calls_to_file(temp_file: str) -> None:
    """Тест: несколько вызовов функции с логированием в файл."""

    @log(filename=temp_file)
    def increment(x: int) -> int:
        return x + 1

    increment(1)
    increment(2)
    increment(3)

    with open(temp_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.strip().split('\n')
        assert len(lines) == 3
        for line in lines:
            assert "increment ok" in line


# -------- ТЕСТЫ НА СОХРАНЕНИЕ МЕТАДАННЫХ --------

def test_log_preserves_function_name() -> None:
    """Тест: декоратор сохраняет имя функции."""

    @log()
    def test_function() -> None:
        pass

    assert test_function.__name__ == "test_function"


def test_log_preserves_function_docstring() -> None:
    """Тест: декоратор сохраняет docstring функции."""

    @log()
    def test_function() -> None:
        """Это тестовая функция."""
        pass

    assert test_function.__doc__ == "Это тестовая функция."


def test_log_preserves_function_signature() -> None:
    """Тест: декоратор сохраняет сигнатуру функции."""

    @log()
    def add(a: int, b: int, c: int = 0) -> int:
        return a + b + c

    import inspect
    sig = inspect.signature(add)
    assert 'a' in sig.parameters
    assert 'b' in sig.parameters
    assert 'c' in sig.parameters
    assert sig.parameters['c'].default == 0

