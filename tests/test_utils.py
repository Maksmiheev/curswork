import unittest
from unittest.mock import patch
from src.utils import (get_card_data, get_currency_rates, get_greeting,
                       get_stock_prices, get_top_transactions)


class TestGetGreeting(unittest.TestCase):
    def test_get_greeting_morning(self):
        greeting = get_greeting("2023-05-15 07:30:00")
        self.assertEqual(greeting, "Доброе утро")

    def test_get_greeting_afternoon(self):
        greeting = get_greeting("2023-05-15 14:00:00")
        self.assertEqual(greeting, "Добрый день")

    def test_get_greeting_evening(self):
        greeting = get_greeting("2023-05-15 20:00:00")
        self.assertEqual(greeting, "Добрый вечер")

    def test_get_greeting_night(self):
        greeting = get_greeting("2023-05-15 01:00:00")
        self.assertEqual(greeting, "Доброй ночи")

class TestGetTopTransactions(unittest.TestCase):
    def test_get_top_transactions_default(self):
        transactions = [
            {"amount": 100}, {"amount": 200}, {"amount": 50}, {"amount": 300}, {"amount": 150}
        ]
        top_transactions = get_top_transactions(transactions)
        expected_output = [
            {"amount": 300}, {"amount": 200}, {"amount": 150}, {"amount": 100}, {"amount": 50}
        ]
        self.assertListEqual(top_transactions, expected_output)

    def test_get_top_transactions_custom_count(self):
        transactions = [
            {"amount": 100}, {"amount": 200}, {"amount": 50}, {"amount": 300}, {"amount": 150}
        ]
        top_transactions = get_top_transactions(transactions, n=3)
        expected_output = [
            {"amount": 300}, {"amount": 200}, {"amount": 150}
        ]
        self.assertListEqual(top_transactions, expected_output)


@patch('requests.get')
class TestGetCurrencyRates(unittest.TestCase):
    def test_get_currency_rates(self, mock_get):
        mock_response = {
            "rates": {"EUR": 0.9, "GBP": 0.8}
        }
        mock_get.return_value.json.return_value = mock_response
        rates = get_currency_rates()
        expected_output = [
            {"currency": "USD", "rate": 1},
            {"currency": "EUR", "rate": 0.9}
        ]
        self.assertEqual(rates, expected_output)


@patch('requests.get')
def test_get_stock_prices(mock_get):
    mock_get.return_value.json.return_value = [
        {'price': 150.0}, {'price': 3000.0}, {'price': 2800.0}, {'price': 200.0}, {'price': 700.0}
    ]


if __name__ == "__main__":
    unittest.main()