from app import create_app
from extensions import db
from model.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    # เช็คก่อนว่ามี admin แล้วหรือยัง
    existing_admin = User.query.filter_by(username="admin01").first()

    if not existing_admin:
        admin = User(
            username="admin01",
            password_hash=generate_password_hash("admin123"),
            first_name="Admin",
            last_name="System",
            role=1   # 1 = admin
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Admin created successfully!")
    else:
        print("⚠️ Admin already exists")
