from extensions import db
from datetime import datetime, timezone

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(
    db.DateTime,
    default=lambda: datetime.now(timezone.utc))
    def __repr__(self):
        return f"<Product {self.name} | Stock: {self.stock}>"
