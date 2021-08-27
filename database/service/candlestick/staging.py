from . import Connection


def add(dataset):
	with Connection('staging').get_connection() as conn:
		conn.execute(
			f"INSERT INTO candlestick ("
			f"open, high, low, close, open_timestamp, close_timestamp"
			f") VALUES ("
			f"{dataset['open']},{dataset['high']},"
			f"{dataset['low']},{dataset['close']},"
			f"'{dataset['open_timestamp']}','{dataset['close_timestamp']}') "
			f"ON DUPLICATE KEY UPDATE "
			f"open = {dataset['open']}, "
			f"high = {dataset['high']}, "
			f"low = {dataset['low']}, "
			f"close = {dataset['close']}, "
			f"open_timestamp = '{dataset['open_timestamp']}', "
			f"close_timestamp = '{dataset['close_timestamp']}' "
		)


def edit(c_id, pattern, signal):
	with Connection('staging').get_connection() as conn:
		conn.execute(
			f"UPDATE candlestick SET "
			f"pattern = '{pattern}', "
			f"signal = '{signal}' "
			f"WHERE candlestick_id = {c_id};"
		)


def read_last_3():
	with Connection('staging').get_connection() as conn:
		result = conn.execute(
			f"SELECT * FROM ("
			f"SELECT * FROM candlestick ORDER BY open_timestamp DESC LIMIT 3"
			f") AS r ORDER BY open_timestamp"
		)
		candles = []
		for r in result:
			candles.append({
				'candlestick_id': r[0],
				'open': r[1],
				'high': r[2],
				'low': r[3],
				'close': r[4],
				'open_timestamp': r[5],
				'close_timestamp': r[6],
			})
		return candles
