class Config:
    # พิมพ์บรรทัดนี้ลงไปแทนของเดิมครับ
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/ecommerce_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret-key"