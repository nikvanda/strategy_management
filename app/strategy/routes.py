from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..controllers import save, get_by_pk, get_user_strategies
from app import Strategy, db


class StrategyListView(MethodView):
    init_every_request = False
    decorators = [jwt_required()]
    methods = ['GET', 'POST']
    model = Strategy

    def get(self):
        user_id = get_jwt_identity()
        related_strategies = get_user_strategies(user_id)
        response = {'user_strategies': [{'name': st.name,
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
        return jsonify({'error': 'Strategy creation failed'})


class StrategyDetailView(StrategyListView):
    methods = ['GET', 'PATCH', 'DELETE']

    def _get_item(self, id):
        return self.model.query.get_or_404(id)

    def get(self, id):
        item = self._get_item(id)
        return jsonify(item.to_json())

    def patch(self, id):
        pass

    def delete(self, id):
        item = self._get_item(id)
        db.session.delete(item)
        db.session.commit()
        return "", 204
