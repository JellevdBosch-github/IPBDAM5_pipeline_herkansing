import utils
import requests
import pandas as pd
from database.service.currency import staging


class ETLCurrency:

	def __init__(self):
		self.base_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol=DOGEEUR"
		self.dataset = self.extract()
		self.dataset = self.transform()
		self.load()

	def extract(self):
		"""
		Extracts the data from the endpoint
		:return: pandas DataFrame of the requested data
		"""
		r = requests.get(self.base_url).json()
		return pd.DataFrame(r, index=[0])

	def transform(self):
		"""
		Transforms the data minimally
		Removes unneeded columns
		:return: cleaned dataset as a Python List
		"""
		df = utils.drop_columns(self.dataset, [
			'weightedAvgPrice',
			'lastQty', 'quoteVolume',
			'bidPrice', 'lowPrice',
			'bidQty',
			'askPrice', 'askQty', 'firstId',
			'lastId', 'count'
		])
		# rounds percentChange column to 2 decimals
		dataset = df.values.tolist()[0]
		dataset[2] = round(float(dataset[2]), 2)
		return dataset

	def load(self):
		"""
		Loads the data into the database using the database services
		Updates existing data
		"""
		dataset = {
			'id': self.dataset[0],
			'price_change': self.dataset[1],
			'price_change_percentage': self.dataset[2],
			'prev_close_price': self.dataset[3],
			'last_price': self.dataset[4],
			'open_price': self.dataset[5],
			'high_price': self.dataset[6],
			'volume': self.dataset[7],
			'open_time': self.dataset[8],
			'close_time': self.dataset[9],
		}
		staging.add(dataset)
