import json
import os
from datetime import datetime
from typing import Any

import requests
import yfinance as yf
from dotenv import load_dotenv

from src.utils import read_xlsx, write_data

api_key = os.getenv("api_key")
load_dotenv()


def get_greeting(hour: Any) -> Any:
    """Возвращает приветсвтие в зависимотси от времени"""
    if hour is None:
        hour = datetime.now()
    else:
        hour = datetime.strptime(hour, "%d.%m.%Y %H:%M")
    hour = hour.hour
    if 5 < hour < 12:
        return "Доброе утро"
    if 12 <= hour < 18:
        return "Добрый день"
    if 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def card_numbers(read: Any) -> Any:
    """Возвращает номер карты пользователя"""
    if read is not None:
        for transact in read:
            return transact["Номер карты"]


def total_sum_amount(data: Any, card_number: Any) -> Any:
    """Возвращает общую сумму всех транзакций пользователя"""
    total = 0
    if card_number:
        for transact in data:
            total += transact["Сумма операции"]
    return round(total)


def cashback(total: int) -> Any:
    """Возвращает cashback"""
    cash = total // 100
    return cash


def top_5_transaction(data: Any) -> Any:
    """Возвращает топ 5 транзакций пользователя"""
    if data is not None:

        def sort_sum(item: Any) -> Any:
            return item["Сумма операции"]

        data.sort(key=sort_sum, reverse=True)
        result = []
        count = 0
        for transaction in data:
            if count < 5:
                result.append(
                    {
                        "date": transaction["Дата операции"],
                        "amount": round(transaction["Сумма операции"]),
                        "category": transaction["Категория"],
                        "description": transaction["Описание"],
                    }
                )
                count += 1
            else:
                break
        return result
    else:
        return None


def get_currency(currency: Any) -> Any:
    """Возвращает курс валют"""
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.get(url, headers={"api_key": api_key}, timeout=15)
    response_data = json.loads(response.text)

    if "rates" in response_data and "RUB" in response_data["rates"]:
        rate = response_data["rates"]["RUB"]
        return rate


def get_stock_currency(stock: str) -> Any:
    """Возвращает курс акций"""
    tiker = yf.Ticker(stock)
    data_today = tiker.history(period="id")
    if not data_today.empty:
        high_price = data_today["High"].iloc[0]
        return high_price
    else:
        return 0.0


def create_operations(greeting: Any, card_number: Any, total_sum: Any, cash: Any, top: Any) -> Any:
    """Возвращает словарь с данными пользователя"""
    data = {"greeting": greeting, "cards": [], "top_transactions": [], "currency_rates": [], "stock_prices": []}
    if read_xlsx("../data/operations.xlsx"):
        if card_number not in [card["last_digits"] for card in data["cards"]] and card_number is not None:
            data["cards"].append({"last_digits": card_number, "total_spent": round(total_sum, 2), "cashback": cash})
        data["top_transactions"] = top

        usd_rate = get_currency("USD")
        eur_rate = get_currency("EUR")

        if usd_rate is not None and eur_rate is not None:
            data["currency_rates"].append(
                (
                    {"currency": "USD", "rate": round(usd_rate, 2)},
                    {"currency": "EUR", "rate": round(eur_rate, 2)},
                )
            )

        data["stock_prices"].append(
            [
                {"stock": "AAPL", "price": round(get_stock_currency("AAPL"), 2)},
                {"stock": "AMZN", "price": round(get_stock_currency("AMZN"), 2)},
                {"stock": "GOOGL", "price": round(get_stock_currency("GOOGL"), 2)},
                {"stock": "MSFT", "price": round(get_stock_currency("MSFT"), 2)},
                {"stock": "TSLA", "price": round(get_stock_currency("TSLA"), 2)},
            ]
        )
    return data


def main_views() -> None:
    """Главная функция в этом модуле"""
    user_currency = input("Какую валюту вы хотели бы добавить к файлу?").split(", ")
    user_stock = input("Какие материалы вы хотели бы добавить к файлу?").split(", ")
    data = {"currency": user_currency, "stock": user_stock}
    write_data("user_settings.json", data)
    time = input("Напишите дату и время(Формат - DD.MM.YYYY HH:MM):")
    greeting = get_greeting(time if time else None)
    card_number = card_numbers(read_xlsx('../data/operations.xlsx'))
    total_sum = total_sum_amount(read_xlsx('../data/operations.xlsx'), card_number)
    cashbacks = cashback(total_sum)
    top_transactions = top_5_transaction(read_xlsx('../data/operations.xlsx'))
    created = create_operations(greeting, card_number, total_sum, cashbacks, top_transactions)
    write_data("new.json", created)
