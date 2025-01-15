from flask import Flask

from config import Config
from .extensions import db, jwt, cache
from .models import User, Strategy, Condition


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.strategy import bp as strategy_bp, strategy_detail_view, strategy_list_view
    app.register_blueprint(strategy_bp)
    app.add_url_rule(f'{strategy_bp.url_prefix}/<int:pk>', view_func=strategy_detail_view)
    app.add_url_rule(strategy_bp.url_prefix, view_func=strategy_list_view)

    return app
