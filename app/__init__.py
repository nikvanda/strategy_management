from flask import Flask

from config import Config
from .extensions import db, jwt
from .models import User, Strategy, Condition


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()

    from app.auth import bp as main_bp
    app.register_blueprint(main_bp)

    return app
