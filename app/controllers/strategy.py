from sqlalchemy import and_

from ..models import Strategy


def get_user_strategies(pk: int):
    return Strategy.query.filter_by(user_id=pk).all()


def get_user_strategy(user_id: int, pk: int):
    return Strategy.query.filter(and_(Strategy.user_id == user_id, Strategy.id == pk)).first()
