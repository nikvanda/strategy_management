import pandas as pd


def simulate_strategy(df: pd.DataFrame, strategy):
    balance, position, entry_price = 0, 0, 0
    trades = []

    for index, row in df.iterrows():
        momentum = row['momentum']
        close_price = row['close']

        if momentum > strategy['buy_conditions']['threshold'] and position == 0:
            position = 1
            entry_price = close_price
            trades.append({'action': 'buy', 'date': row['date'], 'price': close_price})

        elif momentum < strategy['sell_conditions']['threshold'] and position == 1:
            profit = close_price - entry_price
            balance += profit
            position = 0
            trades.append({'action': 'sell', 'date': row['date'], 'price': close_price, 'profit': profit})

    sell_trades = [trade.get('profit', 0) for trade in trades if trade['action'] == 'sell']
    max_drawdown = min(sell_trades) if sell_trades else 0

    return {
        'strategy_id': strategy.id,
        'total_trades': len(trades),
        'profit_loss': balance,
        'win_rate': sum(1 for trade in trades if trade['action'] == 'sell' and trade.get('profit', 0) > 0) / len(
            trades) * 100 if trades else 0,
        'max_drawdown': max_drawdown,
    }


def is_value_repeat(value: list[dict[str, str, float]], repeated_value: str) -> bool:
    tmp = list(map(lambda x: x[repeated_value], value))
    return len(tmp) != len(set(tmp))

