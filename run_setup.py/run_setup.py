from flask import Flask
from extensions import db
from models import User, Product, Order, OrderItem 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()
    print("--- สร้าง Database และ Table สำเร็จแล้ว! ---")

# ตรงนี้แหละครับคือคำสั่งที่ใช้สร้างตาราง
with app.app_context():
    print("กำลังสร้างตารางใน Database...")
    db.create_all()
    print("สร้างเสร็จแล้ว! ไฟล์ ecommerce.db จะปรากฏขึ้นมาครับ")