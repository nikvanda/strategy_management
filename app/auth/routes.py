from flask import request, jsonify
from flask_jwt_extended import create_access_token

from ..controllers import save, get_by_username
from app.auth import bp
from app.models import User


@bp.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if get_by_username(username=username):
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    save(new_user)

    return jsonify({'id': new_user.id, 'username': new_user.username}), 201


@bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = get_by_username(username=username)
    if not user:
        return jsonify({'error': 'No such a user'}), 400

    if user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401
