from flask import Flask

from config import Config
from .extensions import db, jwt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    from app.auth import bp as main_bp
    app.register_blueprint(main_bp)

    @app.route('/')
    def hello_world():  # put application's code here
        return 'Hello World!'

    return app
