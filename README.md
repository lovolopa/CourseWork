# Курсовая Работа

## Веб-страницы

### Главная

1.Функция get_greeting - Возвращает приветсвие в зависимости от времени;-

2.Функция card_numbers - Возвращает номер карты пользователя;

3.Функция total_sum_amount - Возваращет общую сумму всех транзакций пользователя;

4.Функция cashback - Вычесляет кэшбек и вовзращает его;

5.Функция top_5_transaction - Возвращает топ 5 транзакций пользователя;

6.Функция get_currency - Получает курс валюты к рублю; 

7.Функция get_stock_currency получает цену акций на заданную компанию (stock) с помощью yfinance;

8.Функция create_operations - Создаёт словарь с разной информацией(информация о картах, транзакции, курс валют и цены акций);

9.Функция write_data - записывает собранные данные "user_settings.json"

## Сервисы

### Простой поиск

Функция filter_by_state принимает список транзакций и возвращает новый спискок, содержащий только те словари, у которых ключ "Категория" содержит строки "Переводы" и ключ "Описание"

## Отсчёты

### Траты по категории

Функция filter_transactions, принимает на вход DataFrame с транзакциями и категорию расходов, и возвращает сумму расходов по указанной категории.