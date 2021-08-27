from . import Connection


def edit(wallet, action):
	with Connection('staging').get_connection() as conn:
		if action == 'buy':
			conn.execute(
				f"UPDATE wallet SET "
				f"eur_value = eur_value - {wallet['eur_value']}, "
				f"doge_value = doge_value - {wallet['doge_value']}"
			)
		else:
			conn.execute(
				f"UPDATE wallet SET "
				f"eur_value = eur_value + {wallet['eur_value']}, "
				f"doge_value = doge_value + {wallet['doge_value']}"
			)


def read(wallet_id):
	with Connection('staging').get_connection() as conn:
		result = conn.execute(
			f"SELECT eur_value FROM wallet WHERE wallet_id = '{wallet_id}'"
		)
		eur_value = 0.00
		for r in result:
			eur_value = r
		return eur_value[0]
