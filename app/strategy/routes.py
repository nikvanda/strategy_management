import pandas as pd
import sqlalchemy
from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import utils, cache, Strategy, User
from ..controllers import save, get_user_strategies, get_user_strategy, delete, update_strategy, get_by_pk
from app.strategy import bp
from ..extensions import channel


class StrategyListView(MethodView):
    init_every_request = False
    decorators = [jwt_required()]
    methods = ['GET', 'POST']
    model = Strategy

    @cache.cached(timeout=60 ** 2, key_prefix=lambda: f'strategies_{get_jwt_identity()}')
    def get(self):
        user_id = get_jwt_identity()
        related_strategies = get_user_strategies(user_id)
        response = {'user_strategies': [{'id': st.id,
                                         'name': st.name,
                                         'description': st.description,
                                         'asset_type': st.asset_type,
                                         'status': st.status}
                                        for st in related_strategies]}
        return jsonify(response), 200

    def post(self):
        user_id = get_jwt_identity()

        data = request.get_json()
        try:
            sell_conditions = data.pop('sell_conditions')
        except KeyError:
            sell_conditions = {}

        try:
            buy_conditions = data.pop('buy_conditions')
        except KeyError:
            buy_conditions = {}

        try:
            strategy = self.model(user_id=user_id, **data)
            save(strategy)
            update_strategy(strategy, {'sell_conditions': sell_conditions, 'buy_conditions': buy_conditions})
        except (sqlalchemy.exc.DataError, TypeError):
            return jsonify({'error': 'Invalid data'}), 400

        if strategy.id:
            cache.delete(f'strategies_{user_id}')
            user = get_by_pk(user_id, User)
            channel.basic_publish(exchange='',
                                  routing_key='strategy_changed',
                                  body=f'User {user.username} created {strategy.name}.')
            return jsonify({'name': strategy.name, 'asset_type': strategy.asset_type, 'id': strategy.id}), 201
        return jsonify({'error': 'Strategy creation failed'}), 400


class StrategyDetailView(StrategyListView):
    methods = ['GET', 'PATCH', 'DELETE']

    def get(self, pk):
        user_id = get_jwt_identity()
        st = get_user_strategy(user_id, pk)
        if st is None:
            return jsonify({'error': 'No such a strategy'}), 404

        response = st.to_dict()
        return jsonify(response), 200

    def patch(self, pk):
        user_id = get_jwt_identity()
        st = get_user_strategy(user_id, pk)
        if st is None:
            return jsonify({'error': 'No such a strategy'}), 400

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided for update'}), 400

        try:
            update_strategy(st, data)
        except (sqlalchemy.exc.DataError, TypeError):
            return jsonify({'error': 'Invalid data'}), 400
        save(st)

        response = st.to_dict()
        user = get_by_pk(user_id, User)
        cache.delete(f'strategies_{user_id}')
        channel.basic_publish(exchange='',
                              routing_key='strategy_changed',
                              body=f'User {user.username} updated strategy {st.name}.')
        return jsonify(response), 200

    def delete(self, pk):
        user_id = get_jwt_identity()
        st = get_user_strategy(user_id, pk)
        if st is None:
            return jsonify({'error': 'No such a strategy.'}), 400

        delete(st)
        cache.delete(f'strategies_{user_id}')
        return jsonify({'message': 'Successfully delete an object'}), 204


@bp.route('<int:pk>/simulate/', methods=['POST'])
@jwt_required()
def simulate(pk: int):
    user_id = get_jwt_identity()
    st = get_user_strategy(user_id, pk)
    if st is None:
        return jsonify({'error': 'No such a strategy'}), 400

    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({'error': 'Invalid or empty data provided'}), 400

    df = pd.DataFrame(data)
    try:
        df['date'] = pd.to_datetime(df['date'])
    except TypeError:
        return jsonify({'error': 'Some of your provided data does not have date.'}), 400
    try:
        df['momentum'] = df['close'] - df['close'].shift(1)
    except TypeError:
        return jsonify({'error': 'Impossible to calculate momentum. Check provided data.'}), 400

    try:
        result = utils.simulate_strategy(df, st)
    except TypeError:
        return jsonify({'error': 'Some data is in incorrect format.'}), 400
    except IndexError:
        return jsonify(
            {'error': 'To simulate your strategy you must provide buy and sell conditions of the same type'}), 400

    return jsonify(result), 200
