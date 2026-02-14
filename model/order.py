from extensions import db
from datetime import datetime, timezone

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"), 
        nullable=False
    )
