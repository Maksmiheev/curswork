from datetime import datetime
from typing import Dict, List

def analyze_categories(data: List[Dict], year: int, month: int) -> dict:
    """
    Анализирует выгодные категории повышенного кешбэка за указанный месяц и год.
    """
    filtered_data = list(
        filter(
            lambda x: datetime.strptime(x["date"], "%Y-%m-%d").year == year
            and datetime.strptime(x["date"], "%Y-%m-%d").month == month,
            data,
        )
    )

    category_sums = {}
    for transaction in filtered_data:
        cat = transaction["category"]
        amount = transaction["amount"]

        if cat not in category_sums:
            category_sums[cat] = 0

        category_sums[cat] += amount

    return category_sums

def investment_bank(month, transactions, limit):
    filtered = filter(lambda t: t["date"].startswith(month), transactions)

    def round_up(amount):
        return ((int(amount) + limit - 1) // limit) * limit

    savings = sum(round_up(t["amount"]) - t["amount"] for t in filtered)
    return savings

def simple_search(query: str, transactions: List[Dict]) -> List[Dict]:
    """
    Выполняет простой поиск среди транзакций по запросу в категориях и описаниях.
    """
    return list(
        filter(
            lambda tx: query.lower() in tx.get("description", "").lower()
            or query.lower() in tx.get("category", "").lower(),
            transactions,
        )
    )

def search_phone_numbers(transactions: List[Dict]) -> List[Dict]:
    """
    Возвращает транзакции, содержащие мобильный номер телефона.
    """
    return list(
        filter(
            lambda tx: any(word.startswith("+") and word[1:].isdigit() for word in tx.get("description", "").split()),
            transactions,
        )
    )

def find_personal_transfers(transactions: List[Dict]) -> List[Dict]:
    return list(
        filter(
            lambda tx: tx.get("category") == "Переводы"
            and len(tx.get("description", "")) > 0,
            transactions,
        )
    )
