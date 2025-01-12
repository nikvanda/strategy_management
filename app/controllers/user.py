from ..models import User


def get_by_username(username: str):
    return User.query.filter_by(username=username).first()
