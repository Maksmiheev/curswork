import unittest
from src.service import (analyze_categories, find_personal_transfers,
                         investment_bank, search_phone_numbers, simple_search)


class TestAnalyzeCategories(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"date": "2023-05-15", "category": "Еда", "amount": 100},
            {"date": "2023-05-20", "category": "Транспорт", "amount": 50},
            {"date": "2023-06-01", "category": "Развлечения", "amount": 150}
        ]

    def test_analyze_categories_valid_input(self):
        result = analyze_categories(self.data, 2023, 5)
        expected_result = {'Еда': 100, 'Транспорт': 50}
        self.assertEqual(result, expected_result)

    def test_empty_list(self):
        empty_data = []
        result = analyze_categories(empty_data, 2023, 5)
        expected_result = {}
        self.assertEqual(result, expected_result)


class TestInvestmentBank(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {"date": "2023-05-01", "amount": 123},
            {"date": "2023-05-15", "amount": 234},
            {"date": "2023-06-01", "amount": 345}
        ]


    def test_no_matching_month(self):
        result = investment_bank('2023-06', [], 100)
        expected_result = 0
        self.assertEqual(result, expected_result)


class TestSimpleSearch(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {"description": "Оплата продуктов", "category": "Продукты"},
            {"description": "Поездка в такси", "category": "Такси"}
        ]

    def test_simple_search_exact_match(self):
        results = simple_search("продукты", self.transactions)
        self.assertEqual(len(results), 1)
        self.assertIn({"description": "Оплата продуктов", "category": "Продукты"}, results)

    def test_simple_search_no_results(self):
        results = simple_search("кино", self.transactions)
        self.assertEqual(len(results), 0)


class TestSearchPhoneNumbers(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {"description": "+79111234567 Оплата товара"},
            {"description": "Покупка товаров без номера"}
        ]

    def test_search_phone_numbers_with_number(self):
        results = search_phone_numbers(self.transactions)
        self.assertEqual(len(results), 1)
        self.assertIn({"description": "+79111234567 Оплата товара"}, results)

    def test_search_phone_numbers_without_number(self):
        results = search_phone_numbers([{"description": "Нет номера"}])
        self.assertEqual(len(results), 0)


class TestFindPersonalTransfers(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {"category": "Переводы", "description": "Иван Петров"},
            {"category": "Покупки", "description": "Интернет-магазин"}
        ]

    def test_find_personal_transfers_found(self):
        results = find_personal_transfers(self.transactions)
        self.assertEqual(len(results), 1)
        self.assertIn({"category": "Переводы", "description": "Иван Петров"}, results)

    def test_find_personal_transfers_not_found(self):
        results = find_personal_transfers([{"category": "Банковские услуги", "description": "Операция"}])
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()