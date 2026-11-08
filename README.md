# Банковские операции - Маскировка и обработка данных

##  Описание проекта

Проект предоставляет набор инструментов для безопасной работы с банковскими данными. Включает функции для:

- **Маскировки конфиденциальных данных** (номера карт и счетов)
- **Форматирования дат** из ISO формата в удобочитаемый вид
- **Обработки информации о транзакциях** (фильтрация по статусу, сортировка по дате)
- **Фильтрации транзакций по валютам**
- **Генерации номеров банковских карт**
- **Логирования выполнения функций**
### Примеры вызова функций с тестовыми данными находятся в файле example.py  и example_deco.py

Проект разработан в рамках учебного курса

##  Установка и запуск

### Требования
- Python 3.9 или выше
- Poetry (менеджер зависимостей)

### Шаг 1: Клонирование репозитория
#### bash
git clone <https://github.com/LeoCrochet/bank_client_skypro.git>

cd bank-mask-project
### Шаг 2: Установка зависимостей
poetry install
### Шаг 3: Активация виртуального окружения
poetry shell
## Структура проекта

bank_client_skypro/
├── src/                          # Исходный код
│   ├── __init__.py               # Инициализация пакета
│   ├── decorators.py             # Декоратор логирования
│   ├── external_api.py           # Конвертация валют через API
│   ├── file_readers.py           # Чтение CSV и Excel файлов
│   ├── generators.py             # Функции-генераторы данных
│   ├── masks.py                  # Маскировка карт и счетов
│   ├── processing.py             # Обработка транзакций
│   ├── utils.py                  # Чтение данных из JSON
│   └── widget.py                 # Виджеты для работы с данными
├── tests/                        # Модульные тесты
│   ├── __init__.py               # Инициализация пакета
│   ├── test_decorators.py        # Тесты для decorators
│   ├── test_external_api.py      # Тесты для external_api
│   ├── test_file_readers.py      # Тесты для file_readers
│   ├── test_generators.py        # Тесты для generators
│   ├── test_masks.py             # Тесты для masks
│   ├── test_processing.py        # Тесты для processing
│   ├── test_utils.py             # Тесты для utils
│   └── test_widget.py            # Тесты для widget
├── data/                         # Данные для работы
│   ├── operations.json           # JSON с транзакциями
│   ├── transactions.csv          # CSV с транзакциями
│   └── transactions_excel.xlsx   # Excel с транзакциями
├── logs/                         # Логи работы модулей
│   ├── masks.log
│   ├── utils.log
│   └── file_readers.log
├── htmlcov/                      # HTML отчет покрытия
├── pyproject.toml                # Конфигурация проекта
├── .flake8                       # Конфигурация линтера
├── example.py                    # Примеры работы функций
├── example_deco.py               # Примеры работы декоратора
└── README.md                     # Документация  

## Функциональность модулей

### `masks.py` — Маскировка данных
- `get_mask_card_number(card_number)` — маскировка номера карты (XXXX XX** **** XXXX)
- `get_mask_account(account_number)` — маскировка номера счета (**XXXX)

### `widget.py` — Виджеты
- `mask_account_card(account_info)` — маскировка карты или счета в строке
- `get_date(date_string)` — преобразование ISO даты в формат ДД.ММ.ГГГГ

### `processing.py` — Обработка транзакций
- `filter_by_state(transactions, state)` — фильтрация по статусу
- `sort_by_date(transactions, descending)` — сортировка по дате

### `generators.py` — Генераторы
- `filter_by_currency(transactions, currency)` — фильтрация по валюте
- `transaction_descriptions(transactions)` — описания транзакций
- `card_number_generator(start, end)` — генерация номеров карт

### `utils.py` — Чтение JSON
- `get_transactions_from_json(file_path)` — чтение транзакций из JSON

### `file_readers.py` — Чтение CSV и Excel
- `read_transactions_from_csv(file_path)` — чтение транзакций из CSV
- `read_transactions_from_excel(file_path)` — чтение транзакций из Excel (engine `calamine`)

### `external_api.py` — Внешнее API
- `convert_amount_to_rub(transaction)` — конвертация суммы в RUB через API

### `decorators.py` — Логирование
- `log(filename)` — декоратор логирования выполнения функции

## Технологии

- **Python 3.9+** — язык программирования
- **Poetry** — управление зависимостями
- **pandas** — работа с CSV и Excel
- **python-calamine** — движок для чтения Excel
- **requests** — HTTP-запросы к API
- **python-dotenv** — переменные окружения
- **pytest** — тестирование
- **pytest-cov** — покрытие кода
- **Black** — форматирование кода
- **isort** — сортировка импортов
- **Flake8** — линтинг
- **mypy** — проверка типов

## Тесты

### Запуск тестов

```bash
# Все тесты
poetry run pytest tests/ -v

# С покрытием
poetry run pytest tests/ --cov=src --cov-report=term-missing

# HTML отчет покрытия
poetry run pytest tests/ --cov=src --cov-report=html
```

### Покрытие кода

| Файл                          | Stmts   | Пропущено | Покрытие |
|-------------------------------|---------|-----------|----------|
| `src/__init__.py`             | 0       | 0         | 100%     |
| `src/decorators.py`           | 29      | 0         | 100%     |
| `src/external_api.py`         | 31      | 3         | 90%      |
| `src/file_readers.py`         | 44      | 0         | 100%     |
| `src/generators.py`           | 12      | 0         | 100%     |
| `src/masks.py`                | 52      | 2         | 96%      |
| `src/processing.py`           | 21      | 1         | 95%      |
| `src/utils.py`                | 35      | 0         | 100%     |
| `src/widget.py`               | 21      | 1         | 95%      |
| **ИТОГО**                     | **245** | **7**     | **97%**  |

### Описание тестов

| Модуль | Что тестируется |
|--------|-----------------|
| `test_masks.py` | Корректные/некорректные номера карт и счетов, граничные случаи |
| `test_widget.py` | Распознавание карт/счетов, преобразование дат |
| `test_processing.py` | Фильтрация по статусу, сортировка по дате |
| `test_generators.py` | Генераторы валют, описаний, номеров карт |
| `test_utils.py` | Чтение JSON, обработка ошибок |
| `test_file_readers.py` | Чтение CSV и Excel с Mock и patch |
| `test_external_api.py` | Конвертация валют с Mock API |
| `test_decorators.py` | Логирование в консоль и файл |

Все тесты используют **Mock и patch** для изоляции внешних зависимостей (API, файловая система).
## Лицензия
Проект создан в учебных целях.
## Автор
Студент курса Skypro "Leo Crochet"
