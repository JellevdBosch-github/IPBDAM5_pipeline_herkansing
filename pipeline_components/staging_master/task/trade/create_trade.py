import pandas as pd
from uuid import uuid4
import utils
from database.service.trade import staging as trade_service
from database.service.wallet import staging as wallet_service


class CreateTrade:

	def __init__(self, pattern, signal, original_id, candlestick_id, doge_value_batch, close_next):
		self.pattern = pattern
		self.signal = signal
		self.original_id = original_id
		self.candlestick_id = candlestick_id
		self.doge_value_batch = doge_value_batch
		self.close_next = close_next
		self.id = uuid4()
		self.wallet_id = 'b872bab0-88c4-4bbb-8140-daf7180b4d44'
		self.currency_id = 'DOGEEUR'
		self.timestamp = utils.get_current_epoch_ms()
		self.trade()

	def get_id(self):
		return self.id

	def trade(self):
		# If it's a secondary trade
		if self.original_id:
			doge_value = trade_service.read(self.original_id)
			if self.doge_value_batch:
				eur_value = self.doge_value_batch * self.close_next
			else:
				eur_value = utils.convert_currency('DOGE', 'EUR', doge_value)
		# If it's a primary trade
		else:
			eur_value = 100.00
			doge_value = round(utils.convert_currency('EUR', 'DOGE', eur_value), 10)

		eur_value = round(eur_value, 2)
		trade = {
			'trade_id': self.id,
			'wallet_id': self.wallet_id,
			'currency_id': self.currency_id,
			'candlestick_id': self.candlestick_id,
			'pattern': self.pattern,
			'signal': self.signal,
			'eur_value': eur_value,
			'doge_value': doge_value,
			'timestamp': self.timestamp
		}
		wallet = {
			'eur_value': eur_value,
			'doge_value': doge_value,
		}
		if self.original_id:
			wallet_service.edit(wallet, 'buy') if self.signal == 'bear' else wallet_service.edit(wallet, 'sell')
		else:
			wallet_service.edit(wallet, 'buy') if self.signal == 'bull' else wallet_service.edit(wallet, 'sell')

		# If this is a secondary trade
		if self.original_id:
			trade['original_id'] = self.original_id
			trade['wallet_value_eur'] = wallet_service.read(self.wallet_id)
			# Calculate the profits
			if self.signal == 'bull':
				trade['profit'] = trade['eur_value'] - 100.00
			else:
				trade['profit'] = 100.00 - trade['eur_value']
			trade_service.add_secondary(trade)
		else:
			trade_service.add(trade)
