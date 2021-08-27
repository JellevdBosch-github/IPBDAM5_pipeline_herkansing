import utils
import requests
import pandas as pd
from database.service.candlestick import staging


class ETLCandlestickStream:

	def __init__(self):
		self.base_url = f"https://api.binance.com/api/v3/klines?symbol=DOGEEUR&interval=1h"
		self.url = self.url()
		self.dataset = self.extract()
		self.dataset = self.transform()
		self.candle = self.load()

	def get_candle(self):
		return self.candle

	def url(self):
		"""
		Creates the full URL endpoint
		Adds the start time (an hour ago) and the end time (current time)
		:return: URL endpoint
		"""
		current_timestamp = utils.get_current_epoch_ms()
		return f"{self.base_url}" \
			f"&startTime={utils.last_hour_epoch(current_timestamp)}" \
			f"&endTime={current_timestamp}"

	def extract(self):
		"""
		Extracts the data from the endpoint
		:return: pandas DataFrame of the requested data
		"""
		r = requests.get(self.url).json()
		return pd.DataFrame([r[0]],
						columns=['open_timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_timestamp',
								 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
								 'taker_buy_quote_asset_volume', 'ignore'])

	def transform(self):
		"""
		Transforms the data minimally
		Removes unneeded columns
		:return: cleaned dataset as a Python List
		"""
		return utils.drop_columns(self.dataset, [
			'quote_asset_volume',
			'number_of_trades',
			'taker_buy_base_asset_volume',
			'taker_buy_quote_asset_volume',
			'ignore', 'volume'
		]).values.tolist()[0]

	def load(self):
		"""
		Loads the data into the database using the database services
		Replaces any candlestick with the same open timestamp
		"""
		dataset = {
			'open': self.dataset[1],
			'high': self.dataset[2],
			'low': self.dataset[3],
			'close': self.dataset[4],
			'open_timestamp': self.dataset[0],
			'close_timestamp': self.dataset[5],
		}
		staging.add(dataset)
		return dataset
