from ..models import Strategy


def get_user_strategies(pk: int):
    return Strategy.query.filter_by(user_id=pk).all()
