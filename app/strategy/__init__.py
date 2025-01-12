from flask import Blueprint

bp = Blueprint('strategies', __name__, url_prefix='/strategies')

from app.strategy import routes

strategy_list_view = routes.StrategyListView.as_view('strategy-list-view')
strategy_detail_view = routes.StrategyDetailView.as_view('strategy-detail-view')
