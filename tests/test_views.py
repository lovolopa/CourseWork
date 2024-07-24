import json
import unittest
from typing import Any, Dict, List
from unittest import mock
from unittest.mock import patch

from pytest import fixture, mark

from src.utils import read_xlsx
from src.views import (
    card_numbers,
    cashback,
    get_currency,
    get_greeting,
    get_stock_currency,
    top_5_transaction,
    total_sum_amount,
)


@fixture()
def date_with_data() -> Any:
    return read_xlsx("data/operations.xls")


@mark.parametrize(
    "hour, expected",
    [
        ("07.05.2023 08:00", "Доброе утро"),
        ("12.05.2023 13:00", "Добрый день"),
        ("20.05.2023 21:00", "Добрый вечер"),
        ("23.05.2023 00:00", "Доброй ночи"),
    ],
)
def test_greeting(hour: str, expected: str) -> None:
    assert get_greeting(hour) == expected


def test_get_cashback() -> None:
    assert cashback(370) == 3
    assert cashback(0) == 0


@patch("requests.get")
def test_get_currency_rate(mock_get: Any) -> None:
    mock_response = {"rates": {"RUB": 75.0}}
    mock_get.return_value.text = json.dumps(mock_response)
    transaction = {"amount": 100, "currency": "USD"}
    assert get_currency(transaction) == 75.0


def test_get_stock_currency() -> None:
    mock_todays_data = mock.Mock()
    mock_todays_data_dict = [{"High": 100.0}]
    mock_todays_data.to_dict.return_value = mock_todays_data_dict

    with mock.patch("src.views.yf", autospec=True) as mock_yf:
        mock_ticker = mock.Mock()
        mock_yf.Ticker.return_value = mock_ticker
        mock_ticker.history.return_value = mock_todays_data

        result = get_stock_currency("AAPL")

        assert result == 0.0
        mock_yf.Ticker.assert_called_once_with("AAPL")


class TestCardNumberFunction(unittest.TestCase):

    def test_with_transactions(self) -> None:
        transactions: List[Dict[str, Any]] = [
            {"Номер карты": "1234567890123456", "Сумма": 100},
            {"Номер карты": "6543210987654321", "Сумма": 200},
        ]
        self.assertEqual(card_numbers(transactions), "1234567890123456")


class TestTotalSumAmountFunction(unittest.TestCase):

    def test_with_transactions(self) -> None:
        transactions: List[Dict[str, Any]] = []
        self.assertEqual(total_sum_amount(transactions, "1234567890123456"), 0)


class TestTopTransactionFunction(unittest.TestCase):

    def test_with_empty_list(self) -> None:
        transactions: List[Dict[str, Any]] = []
        self.assertEqual(top_5_transaction(transactions), [])
