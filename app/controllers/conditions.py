from app import db


def get_strategy_related(st_pk: int, model: db.Model):
    return model.query.filter_by(strategy_id=st_pk).all()
