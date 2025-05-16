import os

class Config:
    username = "XXX"
    password = "XXX"
    hostname = "XXX"
    port = "3306"
    database = "XXX"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True