import pandas as pd
from uuid import uuid4
import utils


class CreateTrade:

	def __init__(self, pattern, signal, original):
		self.pattern = pattern
		self.signal = signal
		self.original = original
		self.id = uuid4()

	def trade(self):
		trade = {}
		# If it's a secondary trade
		if self.original:
			#		trade['eur_value'] = utils.convert_currency('DOGE', 'EUR', self.doge_value)  # TODO get the dogeamount from somewhere
			# 		trade['doge_value'] = self.doge_value  # TODO get the dogeamount from somewhere
			pass
		# If it's a primary trade
		else:
			trade['eur_value'] = 100.00
			trade['doge_value'] = round(utils.convert_currency('EUR', 'DOGE', trade['eur_value']), 10)
		# TODO make the trade
		# If this is a secondary trade
		if self.original:
			# TODO create trade
			# If the original signal was bullish, then now you have to buy back
			if self.signal == 'bull':
				# TODO update wallet
				pass
			else:
				# TODO update wallet
				pass
		else:
			# TODO create trade
			if self.signal == 'bull':
				# TODO update wallet
				pass
			else:
				# TODO update wallet
				pass
