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

    @cache.cached(timeout=60 ** 2, key_prefix='strategies')
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
            sell_conditions = None

        try:
            buy_conditions = data.pop('buy_conditions')
        except KeyError:
            buy_conditions = None

        try:
            strategy = self.model(user_id=user_id, **data)
            save(strategy)
            update_strategy(strategy, {'sell_conditions': sell_conditions, 'buy_conditions': buy_conditions})
        except sqlalchemy.exc.DataError:
            return jsonify({'error': 'Invalid data'}), 400

        if strategy.id:
            cache.delete('strategies')
            user = get_by_pk(user_id, User)
            channel.basic_publish(exchange='',
                                  routing_key='strategy_changed',
                                  body=f'User {user.username} created {strategy.name}.')
            return jsonify({'name': strategy.name, 'asset_type': strategy.asset_type}), 201
        return jsonify({'error': 'Strategy creation failed'}), 400


class StrategyDetailView(StrategyListView):
    methods = ['GET', 'PATCH', 'DELETE']

    def get(self, pk):
        user_id = get_jwt_identity()
        st = get_user_strategy(user_id, pk)
        if st is None:
            return jsonify({'error': 'No such a strategy'}), 400

        response = st.to_dict()
        return jsonify(response), 200

    def patch(self, pk):
        user_id = get_jwt_identity()
        st = get_user_strategy(user_id, pk)
        if st is None:
            return jsonify({'error': 'No such a strategy'}), 400

        data = request.get_json()
        try:
            update_strategy(st, data)
        except sqlalchemy.exc.DataError:
            return jsonify({'error': 'Invalid data'}), 400
        save(st)

        response = st.to_dict()
        user = get_by_pk(user_id, User)
        cache.delete('strategies')
        channel.basic_publish(exchange='',
                              routing_key='strategy_changed',
                              body=f'User {user.username} updated strategy {st.name}.')
        return jsonify(response), 200

    def delete(self, pk):
        user_id = get_jwt_identity()
        st = get_user_strategy(user_id, pk)
        if st is None:
            return jsonify({'error': 'No such a strategy'}), 400

        delete(st)
        cache.delete('strategies')
        return jsonify({'message': 'Successfully delete an object'}), 204


@bp.route('<int:pk>/simulate/', methods=['POST'])
@jwt_required()
def simulate(pk: int):
    user_id = get_jwt_identity()
    st = get_user_strategy(user_id, pk)
    if st is None:
        return jsonify({'error': 'No such a strategy'}), 400

    data = request.get_json()
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['momentum'] = df['close'] - df['close'].shift(1)
    result = utils.simulate_strategy(df, st)

    return jsonify(result), 200
