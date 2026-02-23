class Config:
    SQLALCHEMY_DATABASE_URI = \
        "mysql+pymysql://root:root@localhost:3306/ecommerce_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret-key"