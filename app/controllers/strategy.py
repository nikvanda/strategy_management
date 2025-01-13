from sqlalchemy import and_

from .. import utils
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
            setattr(obj, field, data.pop(field))

    if data:
        repeated_value = 'indicator'
        conds = get_strategy_related(obj.id, Condition)
        for field in data:
            field_data = data.get(field)
            if not utils.is_value_repeat(field_data, repeated_value):
                for cond in conds:
                    if cond.type == field:
                        delete(cond)
                obj.add_conditions({field: field_data})
