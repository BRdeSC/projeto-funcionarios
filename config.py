import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KET') or 'a_secret_key'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'admin'
    MYSQL_DB = 'funcionarios'