import os
from pathlib import Path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/projects.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Lax'


    MAIL_SERVER = 'mail.iralim.com'
    MAIL_PORT = 993
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kk@moimail.ru'
    MAIL_PASSWORD = 'qJ4qE3sS8bqF3pE8'
    MAIL_DEFAULT_SENDER = 'mail.iralim.com'


  
