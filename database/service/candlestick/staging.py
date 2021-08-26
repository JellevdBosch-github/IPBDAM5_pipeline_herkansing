from . import Connection
from pipeline_components.staging_master.task import candlestick


def add(dataset):
	with Connection('staging').connect() as conn:
		conn.execute(
			f"INSERT INTO candlestick ("
			f"open, high, low, close, open_timestamp, close_timestamp"
			f") VALUES ("
			f"{dataset['open']},{dataset['high']},"
			f"{dataset['low']},{dataset['close']},"
			f"{dataset['open_timestamp']},{dataset['close_timestamp']}) "
			f"ON DUPLICATE KEY UPDATE "
			f"open = {dataset['open']}, "
			f"high = {dataset['high']}, "
			f"low = {dataset['low']}, "
			f"close = {dataset['close']}, "
			f"open_timestamp = {dataset['open_timestamp']}, "
			f"close_timestamp = {dataset['close_timestamp']} "
		)


def add_batch():
	pass
