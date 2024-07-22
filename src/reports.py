from datetime import datetime, timedelta

import pandas as pd

from src.utils import logger_setup

logger = logger_setup()


def read_transaction_from_xlsx(filename: str) -> pd.DataFrame:
    """Чтение финансовых операций из XLSX-файла."""
    logger.info(f"Чтение данных из файла {filename}")
    try:
        return pd.read_excel(filename)
    except FileNotFoundError:
        logger.error(f"Файл {filename} не найден")
        return pd.DataFrame()


def filter_transactions(transactions: pd.DataFrame, category: str, data: str) -> pd.DataFrame:
    """Фильтрация транзакций по категории и дате"""
    date_end = datetime.strptime(data, "%d.%m.%Y") + timedelta(days=90)
    transactions_filter = transactions[
        (transactions["category"] == category)
        & (transactions["data_payment"] >= data)
        & (transactions["data_payment"] < date_end.strftime("d.%m.%Y"))
    ]
    return transactions_filter.to_dict("records")


def main_reports() -> None:
    pass
