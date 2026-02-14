from app import create_app
from extensions import db
from model.user import User

app = create_app()

with app.app_context():
    db.create_all()
    print("Database created successfully!")

    # 🔥 ต้องอยู่ใน context
    admin = User.query.filter_by(username="admin01").first()

    if not admin:
        admin = User(
            username="admin01",
            first_name="Admin",
            last_name="System",
            role=-99
        )
        admin.set_password("password")

        db.session.add(admin)
        db.session.commit()

        print("Admin created!")
    else:
        print("Admin already exists.")
