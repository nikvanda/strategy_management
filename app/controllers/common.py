from app import db


def save(obj):
    db.session.add(obj)
    db.session.commit()


def get_by_pk(pk: int, model: db.Model):
    return model.query.filter_by(id=pk).first()


def delete(obj):
    db.session.delete(obj)
    db.session.commit()
