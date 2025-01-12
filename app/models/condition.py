from sqlalchemy import Enum
from sqlalchemy.orm import relationship, backref

from app import db


class Condition(db.Model):
    __tablename__ = 'condition'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(100), nullable=False)
    threshold = db.Column(db.Numeric(6, 2), nullable=False)
    type = db.Column(Enum('buy', 'sell', name='action_type_enum'), nullable=False)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False)

    strategy = relationship('Strategy', backref=backref('conditions', cascade="all, delete-orphan"))
