import utils
import requests
from pprint import pprint
import pandas as pd
from database.service.candlestick import staging
from config import Config


class ETLCandlestickBatch:

	def __init__(self):
		# start time is 3 years ago, 01-01-2018
		self.base_url = f"https://api.binance.com/api/v3/klines?symbol=DOGEEUR&interval=1h&startTime=1514830707000"
		self.dataset = self.extract()
		self.dataset = self.transform()
		self.load()

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
		return utils.drop_columns(self.dataset, [
			'quote_asset_volume',
			'number_of_trades',
			'taker_buy_base_asset_volume',
			'taker_buy_quote_asset_volume',
			'ignore', 'volume'
		])

	def load(self):
		"""
		Loads the data into the database using the database services
		"""
		path = f"{Config.BASE_PATH}/database/dataset"
		self.dataset.to_csv(f'{path}/batch_candles.csv', index=False)
		staging.add_batch()


t = ETLCandlestickBatch()
