import bcrypt
from flask import request, jsonify
from flask_jwt_extended import create_access_token

from app.auth import bp
from app.models import User
from app.extensions import db


@bp.route('/register/', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password=pw_hash)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"id": new_user.id, "username": new_user.username}), 201


@bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401
