from .task.candlestick.etl_stream import ETLCandlestickStream
from .task.trade.pattern_recognition import PatternRecognition
from .task.trade.create_trade import CreateTrade
from database.service.candlestick import staging as cs


def run_staging():
	pass


def run_hourly():
	# Get the latest candlestick
	ETLCandlestickStream()
	# Get the lastest 3 candles for pattern recognition
	candles = cs.read_last_3()
	if len(candles) >= 3:
		# Recognize patterns
		candle = PatternRecognition(candles).scan_pattern()
		if candle['pattern']:
			cs.edit(candle['candlestick_id'], candle['pattern'], candle['signal'])
			trade_id = CreateTrade(candle['pattern'], candle['signal'], '', candle['candlestick_id'], '', '').get_id()
			CreateTrade(candle['pattern'], candle['signal'], trade_id, candle['candlestick_id'], '', '')


def run_daily():
	pass
