from flask import Flask, jsonify, request
from src.utils import (get_card_data, get_currency_rates, get_greeting,
                   get_stock_prices, get_top_transactions)

app = Flask(__name__)


@app.route("/home", methods=["GET"])
def home():
    datetime_str = request.args.get("datetime")
    if not datetime_str:
        return jsonify({"error": "Параметр 'datetime' отсутствует"}), 400

    greeting = get_greeting(datetime_str)

    # Примеры данных карт и транзакций
    cards = [
        {
            "number": "1234567890125814",
            "transactions": [{"amount": 100}, {"amount": 200}, {"amount": 300}],
        },
        {
            "number": "1234567890127512",
            "transactions": [{"amount": 10}, {"amount": 20}, {"amount": 30}],
        },
    ]

    top_transactions = get_top_transactions(
        [
            {
                "date": "21.12.2021",
                "amount": 1198.23,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {
                "date": "20.12.2021",
                "amount": 829.00,
                "category": "Супермаркеты",
                "description": "Лента",
            },
            {
                "date": "20.12.2021",
                "amount": 421.00,
                "category": "Различные товары",
                "description": "Ozon.ru",
            },
            {
                "date": "16.12.2021",
                "amount": -14216.42,
                "category": "ЖКХ",
                "description": "ЖКУ Квартира",
            },
            {
                "date": "16.12.2021",
                "amount": 453.00,
                "category": "Бонусы",
                "description": "Кешбэк за обычные покупки",
            },
        ]
    )

    card_data = get_card_data(cards)
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()

    result = {
        "greeting": greeting,
        "cards": card_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)
