import unittest
from unittest.mock import patch
from src.app import app

class TestHomeEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_missing_datetime_param(self):
        response = self.app.get("/home")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Параметр 'datetime' отсутствует"})

    @patch("app.get_greeting")
    @patch("app.get_card_data")
    @patch("app.get_currency_rates")
    @patch("app.get_stock_prices")
    @patch("app.get_top_transactions")
    def test_home_success(
        self,
        mock_get_top_transactions,
        mock_get_stock_prices,
        mock_get_currency_rates,
        mock_get_card_data,
        mock_get_greeting,
    ):
        datetime_str = "2021-12-21T10:00:00"

        mock_get_greeting.return_value = "Доброе утро"
        mock_get_card_data.return_value = [{"number": "masked", "balance": 600}]
        mock_get_currency_rates.return_value = {"USD": 75.0}
        mock_get_stock_prices.return_value = {"SBER": 250.0}
        mock_get_top_transactions.return_value = [
            {"date": "21.12.2021", "amount": 1198.23, "category": "Переводы"}
        ]

        response = self.app.get(f"/home?datetime={datetime_str}")

        self.assertEqual(response.status_code, 200)
        json_data = response.json
        self.assertIn("greeting", json_data)
        self.assertIn("cards", json_data)
        self.assertIn("top_transactions", json_data)
        self.assertIn("currency_rates", json_data)
        self.assertIn("stock_prices", json_data)

        self.assertEqual(json_data["greeting"], "Доброе утро")
        self.assertEqual(json_data["cards"], [{"number": "masked", "balance": 600}])
        self.assertEqual(json_data["currency_rates"], {"USD": 75.0})
        self.assertEqual(json_data["stock_prices"], {"SBER": 250.0})
        self.assertEqual(json_data["top_transactions"], [{"date": "21.12.2021", "amount": 1198.23, "category": "Переводы"}])

if __name__ == "__main__":
    unittest.main()