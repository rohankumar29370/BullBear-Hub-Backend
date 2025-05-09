class Config:
    username = "xxx"
    password = "xx"
    hostname = "xxxxxx"
    port = "3306"
    database = "xxxxxxx"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True