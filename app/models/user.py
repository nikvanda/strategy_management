import bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)

    def __init__(self, username: str, password: str):
        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        super().__init__(**{'username': username, 'password': pw_hash.decode('utf-8')})

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def get_related_strategies(self):
        pass

    def __repr__(self):
        return self.username
