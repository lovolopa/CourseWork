import unittest
from typing import Any
from unittest.mock import mock_open, patch

import pandas as pd

from src.reports import filter_transactions, read_transaction_from_xlsx


def test_filter_transactions_empty_result() -> None:
    transactions = pd.DataFrame(
        {"category": ["Food", "Clothes", "Entertainment"], "data_payment": ["01.01.2023", "15.01.2023", "10.03.2023"]}
    )
    category = "Electronics"
    start_date = "01.01.2023"

    filtered_transactions = filter_transactions(transactions, category, start_date)

    assert len(filtered_transactions) == 0


class TestReadTransactionsXlsx(unittest.TestCase):

    @patch("pandas.read_excel")
    @patch("builtins.open", new_callable=mock_open)
    @patch("logging.Logger.error")
    def test_read_transactions_xlsx_file_not_found(
        self, mock_logger_error: Any, mock_open: Any, mock_read_excel: Any
    ) -> None:
        # Настроим mock чтобы он выбрасывал FileNotFoundError
        mock_read_excel.side_effect = FileNotFoundError

        file_path = "non_existent_file.xlsx"
        result = read_transaction_from_xlsx(file_path)

        mock_logger_error.assert_called_with(f"Файл {file_path} не найден")
        self.assertTrue(result.empty)
