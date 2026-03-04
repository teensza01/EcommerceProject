from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from extensions import db
from model.product import Product
import json
import os
SESSION_FILE = "session.json"
def save_session(user_id):
    with open(SESSION_FILE, "w") as f:
        json.dump({"user_id": user_id}, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from model.product import Product
    from model.order import Order
    from model.order_item import OrderItem
    from model.stock_transaction import StockTransaction
    from model.user import User
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
