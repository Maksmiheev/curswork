from flask import Flask, request, jsonify
from src.utils import get_greeting, get_card_data, get_top_transactions, get_currency_rates, get_stock_prices

app = Flask(__name__)


@app.route('/home', methods=['GET'])
def home():
    # Получаем аргумент date_time из запроса
    date_time_str = request.args.get('datetime')

    if not date_time_str:
        return jsonify({"error": "Параметр 'datetime' отсутствует"}), 400

    greeting = get_greeting(date_time_str)
    return jsonify({"message": greeting}), 200


@app.route('/cards', methods=['POST'])
def handle_cards():
    cards = request.json.get('cards', [])
    result = get_card_data(cards)
    return jsonify(result), 200


@app.route('/top-transactions', methods=['POST'])
def top_transactions():
    transactions = request.json.get('transactions', [])
    top_trans = get_top_transactions(transactions)
    return jsonify(top_trans), 200


@app.route('/currencies', methods=['GET'])
def currencies():
    rates = get_currency_rates()
    return jsonify(rates), 200


@app.route('/stocks', methods=['GET'])
def stocks():
    prices = get_stock_prices()
    return jsonify(prices), 200


if __name__ == '__main__':
    app.run(debug=True)