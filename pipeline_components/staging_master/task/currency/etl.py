import utils
import requests
import pandas as pd
import database.service.candlestick


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
		df = df.values.tolist()[0]
		df[2] = round(float(df[2]), 2)
		return df

	def load(self):
		"""
		Loads the data into the database using the database services
		Updates existing data
		"""
		print(self.dataset)


t = ETLCurrency()
