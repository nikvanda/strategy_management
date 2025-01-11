from sqlalchemy import Enum

from app import db


class Strategy(db.Model):
    __tablename__ = 'strategy'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    asset_type = db.Column(db.String(50), nullable=False)
    status = db.Column(Enum('active', 'closed', 'paused', name='status_type_enum'), default='active')
