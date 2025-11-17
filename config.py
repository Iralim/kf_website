import os
from pathlib import Path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/projects.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Базовая папка для загрузки изображений (filesystem)
    # Мы будем сохранять относительные пути в БД вида "house_images/<id>/file.jpg"
    # UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "house_images")
