class Config:
    SQLALCHEMY_DATABASE_URI = \
        "mysql+pymysql://root@localhost/ecommerce_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret-key"
