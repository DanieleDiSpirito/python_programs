from flask import Flask, render_template, request, redirect, url_for, jsonify
from upstash_redis import Redis
from dotenv import load_dotenv
import json
import random
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Initialize Redis from environment variables
load_dotenv()
redis = Redis.from_env()

# Initialize the application data if it doesn't exist
def init_app_data():
    # Check if app is already initialized
    if not redis.exists("app:initialized"):
        # Initial wallet with 10,000€
        wallet = {
            "total": 10000,
            "invested": 0,
            "uninvested": 10000,
            "history": [{"date": datetime.now().strftime("%Y-%m-%d"), "value": 10000}]
        }
        redis.set("wallet", json.dumps(wallet))
        
        # Create some sample stocks
        stocks = {
            "AAPL": {"name": "Apple Inc.", "price": 150.0, "history": []},
            "MSFT": {"name": "Microsoft Corp.", "price": 300.0, "history": []},
            "GOOGL": {"name": "Alphabet Inc.", "price": 2800.0, "history": []},
            "AMZN": {"name": "Amazon.com Inc.", "price": 3300.0, "history": []},
            "TSLA": {"name": "Tesla Inc.", "price": 900.0, "history": []}
        }
        
        # Add 30 days of history for each stock
        current_date = datetime.now()
        for symbol, stock_data in stocks.items():
            price = stock_data["price"]
            for i in range(30):
                date = (current_date - timedelta(days=29-i)).strftime("%Y-%m-%d")
                # Random price fluctuation between -3% and +3%
                price_change = price * (1 + (random.random() * 0.06 - 0.03))
                price = round(price_change, 2)
                stock_data["history"].append({"date": date, "price": price})
            stock_data["price"] = price
            redis.set(f"stock:{symbol}", json.dumps(stock_data))
        
        # Initialize portfolio (empty)
        portfolio = {}
        redis.set("portfolio", json.dumps(portfolio))
        
        # Set current date
        redis.set("current_date", current_date.strftime("%Y-%m-%d"))
        
        # Mark as initialized
        redis.set("app:initialized", "1")

# Routes
@app.route('/')
def home():
    init_app_data()
    wallet = json.loads(redis.get("wallet"))
    portfolio = json.loads(redis.get("portfolio"))
    current_date = redis.get("current_date")
    
    return render_template('home.html', 
                          wallet=wallet, 
                          portfolio=portfolio, 
                          current_date=current_date)

@app.route('/buy-sell')
def buy_sell():
    init_app_data()
    wallet = json.loads(redis.get("wallet"))
    portfolio = json.loads(redis.get("portfolio"))
    
    # Get all stocks
    stocks = {}
    for key in redis.keys("stock:*"):
        symbol = key.split(":")[1]
        stocks[symbol] = json.loads(redis.get(key))
    
    selected_stock = request.args.get('stock', 'AAPL')
    stock_data = json.loads(redis.get(f"stock:{selected_stock}"))
    
    return render_template('buy_sell.html', 
                          wallet=wallet, 
                          portfolio=portfolio, 
                          stocks=stocks, 
                          selected_stock=selected_stock,
                          stock_data=stock_data)

@app.route('/api/buy', methods=['POST'])
def buy_stock():
    symbol = request.form.get('symbol')
    quantity = int(request.form.get('quantity'))
    
    stock_data = json.loads(redis.get(f"stock:{symbol}"))
    wallet = json.loads(redis.get("wallet"))
    portfolio = json.loads(redis.get("portfolio"))
    
    total_cost = stock_data["price"] * quantity
    
    # Check if user has enough money
    if wallet["uninvested"] >= total_cost:
        # Update wallet
        wallet["uninvested"] -= total_cost
        wallet["invested"] += total_cost
        
        # Update portfolio
        if symbol in portfolio:
            portfolio[symbol]["quantity"] += quantity
            portfolio[symbol]["avg_price"] = ((portfolio[symbol]["avg_price"] * portfolio[symbol]["quantity"]) + 
                                             (stock_data["price"] * quantity)) / (portfolio[symbol]["quantity"] + quantity)
        else:
            portfolio[symbol] = {
                "name": stock_data["name"],
                "quantity": quantity,
                "avg_price": stock_data["price"]
            }
        
        redis.set("wallet", json.dumps(wallet))
        redis.set("portfolio", json.dumps(portfolio))
        
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Not enough funds"})

@app.route('/api/sell', methods=['POST'])
def sell_stock():
    symbol = request.form.get('symbol')
    quantity = int(request.form.get('quantity'))
    
    stock_data = json.loads(redis.get(f"stock:{symbol}"))
    wallet = json.loads(redis.get("wallet"))
    portfolio = json.loads(redis.get("portfolio"))
    
    # Check if user has enough stocks
    if symbol in portfolio and portfolio[symbol]["quantity"] >= quantity:
        total_value = stock_data["price"] * quantity
        
        # Update wallet
        wallet["uninvested"] += total_value
        wallet["invested"] -= total_value
        
        # Update portfolio
        portfolio[symbol]["quantity"] -= quantity
        if portfolio[symbol]["quantity"] == 0:
            del portfolio[symbol]
        
        redis.set("wallet", json.dumps(wallet))
        redis.set("portfolio", json.dumps(portfolio))
        
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Not enough stocks"})

@app.route('/api/advance-day', methods=['POST'])
def advance_day():
    # Get current data
    current_date_str = redis.get("current_date")
    current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    next_date = current_date + timedelta(days=1)
    next_date_str = next_date.strftime("%Y-%m-%d")
    
    # Update all stock prices
    all_stocks = {}
    for key in redis.keys("stock:*"):
        symbol = key.split(":")[1]
        stock_data = json.loads(redis.get(key))
        
        # Random price fluctuation between -3% and +3%
        price_change = stock_data["price"] * (1 + (random.random() * 0.06 - 0.03))
        new_price = round(price_change, 2)
        
        # Update price and history
        stock_data["price"] = new_price
        stock_data["history"].append({"date": next_date_str, "price": new_price})
        
        redis.set(key, json.dumps(stock_data))
        all_stocks[symbol] = stock_data
    
    # Update wallet value
    wallet = json.loads(redis.get("wallet"))
    portfolio = json.loads(redis.get("portfolio"))
    
    # Calculate new invested value
    new_invested_value = 0
    for symbol, data in portfolio.items():
        new_invested_value += all_stocks[symbol]["price"] * data["quantity"]
    
    # Update wallet
    wallet["invested"] = new_invested_value
    wallet["total"] = wallet["invested"] + wallet["uninvested"]
    wallet["history"].append({"date": next_date_str, "value": wallet["total"]})
    
    redis.set("wallet", json.dumps(wallet))
    redis.set("current_date", next_date_str)
    
    return jsonify({
        "success": True, 
        "new_date": next_date_str,
        "wallet": wallet
    })

@app.route('/api/wallet-history')
def wallet_history():
    wallet = json.loads(redis.get("wallet"))
    return jsonify(wallet["history"])

@app.route('/api/stock-history/<symbol>')
def stock_history(symbol):
    stock_data = json.loads(redis.get(f"stock:{symbol}"))
    return jsonify(stock_data["history"])

if __name__ == '__main__':
    app.run(debug=True)
