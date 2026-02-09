import datetime
import requests


def get_greeting(datetime_str):
    dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    hour = dt.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_data(cards):
    card_data = []
    for card in cards:
        total_spent = sum(transaction["amount"] for transaction in card["transactions"])
        cashback = round(total_spent / 100, 2)
        card_data.append(
            {
                "last_digits": str(card["number"])[-4:],
                "total_spent": round(total_spent, 2),
                "cashback": cashback,
            }
        )
    return card_data


def get_top_transactions(transactions, n=5):
    sorted_transactions = sorted(transactions, key=lambda x: abs(x["amount"]), reverse=True)[:n]
    return sorted_transactions


def get_currency_rates():
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    rates = response.json()["rates"]
    currency_rates = [
        {"currency": "USD", "rate": 1},
        {"currency": "EUR", "rate": rates["EUR"]},
    ]
    return currency_rates


def get_stock_prices():
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    stock_prices = []
    for stock in stocks:
        response = requests.get(f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey=YOUR_API_KEY")
        price = response.json()[0]["price"]
        stock_prices.append({"stock": stock, "price": price})
    return stock_prices
