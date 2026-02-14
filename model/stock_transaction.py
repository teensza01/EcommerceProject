from extensions import db
from datetime import datetime, timezone

class StockTransaction(db.Model):
    __tablename__ = "stock_transactions"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    type = db.Column(db.String(20)) 
    created_at = db.Column(db.DateTime)
    product = db.relationship("Product", backref="stock_transactions")