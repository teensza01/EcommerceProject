from app import create_app
from extensions import db
from model.product import Product
from model.order import Order
from model.order_item import OrderItem

app = create_app()

with app.app_context():

    # สร้างสินค้า
    p = Product(name="Mocha", price=70, stock=10)
    db.session.add(p)
    db.session.commit()

    # เริ่ม Order
    order = Order()
    db.session.add(order)
    db.session.flush()

    quantity = 2

    if p.stock >= quantity:
        p.stock -= quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=p.id,
            quantity=quantity,
            price=p.price
        )

        db.session.add(order_item)
        db.session.commit()

        print("Order Success ✅")
    else:
        print("Stock ไม่พอ ❌")
