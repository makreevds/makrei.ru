from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import os

# SQLAlchemy объект создаётся вне create_app, чтобы избежать циклических импортов
# и давать к нему доступ во всех файлах приложения
db = SQLAlchemy()

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')


def create_app():
    root = Path(__file__).parent.parent.resolve()
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(root / 'templates'),
        static_folder=str(root / 'static')
    )
    instance_dir = Path(app.instance_path)
    instance_dir.mkdir(exist_ok=True)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{instance_dir / "blog.sqlite3"}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app


def init_db():
    from . import db
    app = create_app()
    with app.app_context():
        db.create_all()
        print("База данных успешно инициализирована!")
