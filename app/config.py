import os


class Config:
    # Database configuration
    username = "XXX"
    password = "XXX"
    hostname = "XXX"
    port = "3306"
    database = "XXX"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # JWT configuration
    JWT_SECRET_KEY = 'your-secret-key'  
    JWT_ACCESS_TOKEN_EXPIRES = 3600  