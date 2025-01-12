from sqlalchemy import and_

from ..models import Strategy, Condition
from .common import delete
from .conditions import get_strategy_related


def get_user_strategies(pk: int):
    return Strategy.query.filter_by(user_id=pk).all()


def get_user_strategy(user_id: int, pk: int):
    return Strategy.query.filter(and_(Strategy.user_id == user_id, Strategy.id == pk)).first()


def update_strategy(obj: Strategy, data: dict[str, str, float, list[dict: str, str, float]]):
    base_fields = ['name', 'description', 'asset_type', 'status']
    for field in base_fields:
        if data.get(field):
            setattr(obj, field, data.get(field))

    related_fields = ['buy_conditions', 'sell_conditions']
    is_condition_updated = data.get(related_fields[0]) or data.get(related_fields[1])
    if is_condition_updated:
        conds = get_strategy_related(obj.id, Condition)
        for cond in conds:
            delete(cond)
        obj.add_conditions({'sell': data.get('sell_conditions'),
                            'buy': data.get('buy_conditions')})
