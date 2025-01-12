from sqlalchemy import Enum
from sqlalchemy.orm import relationship

from app import db
from .condition import Condition


class Strategy(db.Model):
    __tablename__ = 'strategy'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    asset_type = db.Column(db.String(50), nullable=False)
    status = db.Column(Enum('active', 'closed', 'paused', name='status_type_enum'), default='active')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = relationship('User', backref='strategies')

    def __init__(self, user_id: int, name: str, description: str, asset_type: str, status: str):
        super().__init__(**{'user_id': user_id, 'name': name, 'description': description,
                            'asset_type': asset_type, 'status': status})

    def __repr__(self):
        return f'Strategy: {self.name}'

    def add_conditions(self, conditions: dict[str, list[dict[str, str, int]] | None]):
        for cond_type, cond_data in conditions.items():
            if cond_data is not None:
                for cond in cond_data:
                    condition = Condition(strategy_id=self.id, type=cond_type, **cond)
                    db.session.add(condition)
                    db.session.commit()
