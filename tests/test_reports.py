import unittest
from datetime import datetime
from unittest.mock import mock_open, patch
import pandas as pd

from src.reports import (get_three_months_ago, report_writer,
                         spending_by_category, spending_by_weekday,
                         spending_by_workday)


class TestReportsModule(unittest.TestCase):
    def setUp(self):
        # Пример датафрейма с транзакциями
        data = {
            "date": [
                "2023-01-01",
                "2023-01-02",
                "2023-01-03",
                "2023-01-04",
                "2023-01-05",
            ],
            "category": ["Food", "Transport", "Food", "Entertainment", "Food"],
            "amount": [100, 50, 150, 200, 120],
        }
        self.transactions = pd.DataFrame(data)
        self.transactions["date"] = pd.to_datetime(self.transactions["date"])

    def test_get_three_months_ago(self):
        # Тестирование функции get_three_months_ago
        with patch("src.reports.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 10, 1)
            result = get_three_months_ago()
            expected = datetime(2023, 7, 1)
            self.assertEqual(result, expected)

    def test_spending_by_category(self):
        # Тестирование функции spending_by_category
        result = spending_by_category(self.transactions)
        expected = (
            self.transactions.groupby("category")["amount"]
            .sum()
            .reset_index(name="total_amount")
        )
        pd.testing.assert_frame_equal(result, expected)

    def test_spending_by_weekday(self):
        # Тестирование функции spending_by_weekday
        result = spending_by_weekday(self.transactions)
        expected = (
            self.transactions.groupby(self.transactions["date"].dt.weekday)["amount"]
            .mean()
            .rename_axis(index={"date": "weekday"})
        )
        pd.testing.assert_series_equal(result, expected)

    def test_spending_by_workday(self):
        expected = (
            self.transactions.assign(
                is_workday=self.transactions["date"].dt.weekday.isin([0, 1, 2, 3, 4])
            )
            .groupby("is_workday")["amount"]
            .mean()
        )
        expected.index.name = "is_workday"  # Та же установка имени
        result = spending_by_workday(self.transactions)
        pd.testing.assert_series_equal(result, expected)

    def test_report_writer(self):
        # Тестирование декоратора report_writer
        @report_writer()
        def test_function():
            return pd.DataFrame({"A": [1, 2, 3]})

        with patch("builtins.open", mock_open()) as mock_file:
            result = test_function()
            mock_file.assert_called_once()
            self.assertIsInstance(result, pd.DataFrame)


if __name__ == "__main__":
    unittest.main()



