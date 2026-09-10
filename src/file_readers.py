import pandas as pd

def read_transactions_from_csv(file_path):
    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        transactions = df.to_dict(orient='records')

        print(f"CSV-файл успешно прочитан: {file_path}, транзакций: {len(transactions)}")
        return transactions

    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as e:
        print(f"Ошибка при чтении CSV-файла {file_path}: {type(e).__name__} - {e}")
        return []

def read_transactions_from_excel(file_path):
    try:
        # ✅ Используем calamine вместо openpyxl
        df = pd.read_excel(file_path, engine='calamine')
        transactions = df.to_dict(orient='records')

        print(f"Excel-файл успешно прочитан: {file_path}, транзакций: {len(transactions)}")
        return transactions

    except (ValueError, KeyError, UnicodeDecodeError) as e:
        print(f"Ошибка при чтении Excel-файла {file_path}: {type(e).__name__} - {e}")
        return []