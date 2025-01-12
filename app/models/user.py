import bcrypt
from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)

    def __init__(self, username: str, password: str):
        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        super().__init__(**{'username': username, 'password': pw_hash})

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, pk: int):
        return cls.query.filter_by(id=pk).first()

    def __repr__(self):
        return self.username
