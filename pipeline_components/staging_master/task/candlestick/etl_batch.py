import utils
import requests
from pprint import pprint
import pandas as pd
from database.service.candlestick import staging
from config import Config


def load(dataset):
	"""
	Loads the data into the database using the database services
	"""
	for candle in dataset:
		staging.add_batch({
			'open': candle['open'],
			'high': candle['high'],
			'low': candle['low'],
			'close': candle['close'],
			'open_timestamp': candle['open_timestamp'],
			'close_timestamp': candle['close_timestamp'],
			'pattern': candle['pattern'],
			'candlestick_signal': candle['signal']
		})


class ETLCandlestickBatch:

	def __init__(self):
		# start time is 3 years ago, 01-01-2018
		self.base_url = f"https://api.binance.com/api/v3/klines?symbol=DOGEEUR&interval=1h" \
						f"&startTime={utils.twentynine_hours_ago_epoch(utils.get_current_epoch_ms())}"
		self.dataset = self.extract()
		self.dataset = self.transform()

	def extract(self):
		"""
		Extracts the data from the endpoint
		:return: pandas DataFrame of the requested data
		"""
		r = requests.get(self.base_url).json()
		return pd.DataFrame(r,
						columns=['open_timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_timestamp',
								 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
								 'taker_buy_quote_asset_volume', 'ignore'])

	def transform(self):
		"""
		Transforms the data minimally
		Removes unneeded columns
		:return: cleaned dataset as a Python List
		"""
		datalist = utils.drop_columns(self.dataset, [
			'quote_asset_volume',
			'number_of_trades',
			'taker_buy_base_asset_volume',
			'taker_buy_quote_asset_volume',
			'ignore', 'volume'
		]).values.tolist()
		candles = []
		for candle in datalist:
			candles.append({
				'open': float(candle[1]),
				'high': float(candle[2]),
				'low': float(candle[3]),
				'close': float(candle[4]),
				'open_timestamp': candle[0],
				'close_timestamp': candle[5],
			})
		return candles

	def get_candles(self):
		return self.dataset
