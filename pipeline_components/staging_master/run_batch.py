from .task.candlestick import etl_batch
from .task.trade.pattern_recognition import PatternRecognition
from .task.trade.create_trade import CreateTrade
from database.service.candlestick import staging as cs
import utils


def run():
	# Get the candlestick batch
	etl = etl_batch.ETLCandlestickBatch()
	candles = etl.get_candles()
	# Recognize patterns
	candles = PatternRecognition(candles).scan_patterns_historical()
	etl_batch.load(candles)
	candles = cs.browse()
	# Loop through every candle
	for i in range(len(candles)):
		# If the candle has a pattern AND there is a next candle, else you cant determine the profit of the trade
		if candles[i]['pattern'] and candles[i+1]:
			# Create the primary trade
			trade_id = CreateTrade(candles[i]['pattern'], candles[i]['signal'], '', candles[i]['candlestick_id'], '', '').get_id()
			# Get the closing price of the NEXT candle in order to determine the profit
			doge_amount = 100 / candles[i]['close']
			# Create the secondary trade
			CreateTrade(candles[i]['pattern'], candles[i]['signal'], trade_id,
						candles[i]['candlestick_id'], doge_amount, candles[i+1]['close'])

