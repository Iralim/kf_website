import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # config.py должен быть в корне проекта

    @app.template_filter('money')
    def money_format(value):
        """Форматирует число с пробелами между тысячами"""
        if value is None:
            return ""
        try:
            return f"{int(value):,}".replace(",", " ")
        except (ValueError, TypeError):
            return value

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Log in to access.'

    from .auth import auth_bp
    from.admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()


    return app
