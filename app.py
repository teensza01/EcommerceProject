from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from extensions import db
from model.product import Product


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from model.product import Product
    from model.order import Order
    from model.order_item import OrderItem
    from model.stock_transaction import StockTransaction
    from model.user import User

    
    @app.route("/products")
    def show_products():
        products = Product.query.all()
        return "<br>".join([
            f"{p.name} | ราคา: {p.price} | คงเหลือ: {p.stock}"
            for p in products
        ])

    @app.shell_context_processor
    def make_shell_context():
        return {"db": db, "Product": Product}


    
    
    
    
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
