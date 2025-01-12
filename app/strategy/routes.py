from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..controllers import save, get_user_strategies, get_user_strategy, get_strategy_related, delete, update_strategy
from app import Strategy, Condition


class StrategyListView(MethodView):
    init_every_request = False
    decorators = [jwt_required()]
    methods = ['GET', 'POST']
    model = Strategy

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

        strategy = self.model(user_id=user_id, **data)
        save(strategy)
        strategy.add_conditions({'sell': sell_conditions, 'buy': buy_conditions})

        if strategy.id:
            return jsonify({'name': strategy.name, 'asset_type': strategy.asset_type}), 201
        return jsonify({'error': 'Strategy creation failed'}), 400


class StrategyDetailView(StrategyListView):
    methods = ['GET', 'PATCH', 'DELETE']

    def get(self, pk):
        user_id = get_jwt_identity()
        st = get_user_strategy(user_id, pk)

        response = st.to_dict()
        return jsonify(response), 200

    def patch(self, pk):
        user_id = get_jwt_identity()
        data = request.get_json()
        st = get_user_strategy(user_id, pk)

        update_strategy(st, data)
        save(st)

        response = st.to_dict()
        return jsonify(response), 200

    def delete(self, pk):  # ToDO: check related objects deletion
        user_id = get_jwt_identity()
        st = get_user_strategy(user_id, pk)
        delete(st)
        return jsonify({'message': 'Successfully delete an object'}), 204
