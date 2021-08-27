from . import Connection


def add(dataset):
	with Connection('staging').get_connection() as conn:
		conn.execute(
			f"INSERT INTO currency "
			f"VALUES ("
			f"'{dataset['id']}',{dataset['price_change']},"
			f"{dataset['price_change_percentage']},{dataset['prev_close_price']},"
			f"{dataset['last_price']},{dataset['open_price']},"
			f"{dataset['high_price']},{dataset['volume']},"
			f"{dataset['open_time']},{dataset['close_time']}) "
			f"ON DUPLICATE KEY UPDATE "
			f"currency_id = '{dataset['id']}', "
			f"price_change = {dataset['price_change']}, "
			f"price_change_percentage = {dataset['price_change_percentage']}, "
			f"prev_close_price = {dataset['prev_close_price']}, "
			f"last_price = {dataset['last_price']}, "
			f"high_price = {dataset['high_price']}, "
			f"volume = {dataset['volume']}, "
			f"open_time = {dataset['open_time']}, "
			f"close_time = {dataset['close_time']}"
		)
