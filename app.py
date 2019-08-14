from flask import Flask, redirect, request, jsonify, make_response, send_file
from flask_heroku import Heroku
from datetime import datetime
from stockengine.stock import Stock
from stockengine.search import search_stock
from werkzeug import exceptions

app = Flask(__name__)
heroku = Heroku(app)

app.secret_key = 'eO\xd93\x9a+"5/u\xfdk7\xe1;)'

########## INFO ROUTES ##########

# Root route
@app.route("/")
def home():
    return "StockEngine"

# Stock profile
@app.route("/stock/<symbol>")
def show_stock(symbol):
    stock = Stock(symbol)
    return jsonify(stock.profile())

# Intraday
@app.route("/stock/<symbol>/intraday")
def show_intraday(symbol):
    stock = Stock(symbol)
    return jsonify(stock.intraday_time_series())

# Daily
@app.route("/stock/<symbol>/daily")
def show_daily(symbol):
    stock = Stock(symbol)
    return jsonify(stock.daily_time_series())

# Monthly
@app.route("/stock/<symbol>/monthly")
def show_monthly(symbol):
    stock = Stock(symbol)
    return jsonify(stock.monthly_time_series())

# Search
@app.route("/stock/title/<name>")
def search_symbol(name):
    stock = Stock(search_stock(name))
    return jsonify(stock.profile())

########## CHART ROUTES ##########

# @app.route("/stock/<symbol>/<block>/chart/<group>")
# def daily_chart(symbol, block, group):
#     img_req = generate_chart(symbol, group, block)
#     if img_req["status"] == 400:
#         return make_response(jsonify(img_req), 404)
#     else:
#         return send_file(img_req["filename"], mimetype='image/png')

########## ERRORS ##########

@app.errorhandler(404)
def handle_bad_request(e):
    return make_response(jsonify({'error': 'Not founded'}), 404)

if __name__ == "__main__":
    # host="0.0.0.0", port=5000, debug=True
    app.run(debug=True)
