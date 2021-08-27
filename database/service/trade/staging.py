from . import Connection


def add(trade):
	with Connection('staging').get_connection() as conn:
		conn.execute(
			f"INSERT INTO trade ("
			f"trade_id, wallet_id, currency_id, candlestick_id, pattern, signal, eur_value, doge_value, timestamp "
			f") VALUES ("
			f"'{trade['trade_id']}', '{trade['wallet_id']}', "
			f"'{trade['currency_id']}', '{trade['candlestick_id']}', "
			f"'{trade['pattern']}', '{trade['signal']}', "
			f"{trade['eur_value']}, {trade['doge_value']}, "
			f"'{trade['timestamp']}') "
		)


def add_secondary(trade):
	with Connection('staging').get_connection() as conn:
		conn.execute(
			f"INSERT INTO trade VALUES ("
			f"'{trade['trade_id']}', '{trade['wallet_id']}', "
			f"'{trade['currency_id']}', '{trade['original_id']}', "
			f"'{trade['candlestick_id']}', "
			f"'{trade['pattern']}', '{trade['signal']}', "
			f"{trade['eur_value']}, {trade['doge_value']}, "
			f"'{trade['timestamp']}', {trade['profit']}, "
			f"{trade['wallet_value_eur']}) "
		)


def read(trade_id):
	with Connection('staging').get_connection() as conn:
		result = conn.execute(
			f"SELECT doge_value FROM trade WHERE trade_id = {trade_id}"
		)
		doge = 0.00
		for r in result:
			doge = r
		return doge
