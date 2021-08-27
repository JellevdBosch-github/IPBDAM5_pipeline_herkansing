from .task.candlestick.etl_stream import ETLCandlestickStream
from .task.currency.etl import ETLCurrency
from .task.trade.pattern_recognition import PatternRecognition
from .task.trade.create_trade import CreateTrade
from database.service.candlestick import staging as cs
import time
import schedule
import datetime


def run_staging():
	schedule.every().hour.at(':59').do(run_hourly())
	schedule.every().day.at('09:00').do(run_daily())
	while True:
		schedule.run_pending()
		time.sleep(20)


def run_hourly():
	"""
	Manages the hourly candlestick ETL process and trading process
	:return: None
	"""
	if datetime.datetime.today().minute == 59:
		# Get the latest candlestick
		ETLCandlestickStream()
		if 7 < datetime.datetime.today().hour < 21:
			# Get the lastest 3 candles for pattern recognition
			candles = cs.read_last_3()
			if len(candles) >= 3:
				# Recognize patterns
				candle = PatternRecognition(candles).scan_pattern()
				if candle['pattern']:
					print(f"Signal given: {candle['signal']} | Pattern given: {candle['pattern']}")
					cs.edit(candle['candlestick_id'], candle['pattern'], candle['signal'])
					trade_id = CreateTrade(candle['pattern'], candle['signal'], '', candle['candlestick_id'], '', '').get_id()
					time.sleep(3570)
					CreateTrade(candle['pattern'], candle['signal'], trade_id, candle['candlestick_id'], '', '')


def run_daily():
	ETLCurrency()
