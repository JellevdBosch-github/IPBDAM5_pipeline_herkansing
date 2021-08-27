def patterns(cur, prev, prev2):
	"""
	Gets 3 candles: the 3 latest ones
	Checks for the most recent candle if it's any of the patterns below
	If it is a pattern then that pattern en the signal (bull/bearish) gets appended to that list
	:param cur: The current or latest candle
	:param prev: The current or latest candle-1
	:param prev2: The current or latest candle-2
	:return: The current candle with the recognized pattern and signal
	"""
	pattern = None
	signal = None

	# open - close
	real_body = abs(cur['open'] - cur['low'])
	# high - low
	candle_range = cur['high'] - cur['low']

	# Bullish Swing
	# if current low > previous low and previous low < previous2 low
	if cur['low'] > prev['low'] and prev['low'] < prev2['low']:
		pattern = 'bullish swing'
		signal = 'bull'
		cur['pattern'] = pattern
		cur['signal'] = signal
	# Bearish Swing
	# if current high < previous high and previous high > previous2 high
	elif cur['high'] < prev['high'] and prev['high'] > prev2['high']:
		pattern = 'bearish swing'
		signal = 'bear'
		cur['pattern'] = pattern
		cur['signal'] = signal
	# Bullish Pinbar
	# if body <= (range / 3) and min(open, close) > (high + low) / 2 and current low < previous low
	# if the real body is smaller than a third of the range and the body is located in the upper half
	elif real_body <= (candle_range / 3) and min(cur['open'], cur['close']) > ((cur['high'] + cur['low']) / 2) and cur['low'] < prev['low']:
		pattern = 'bullish pinbar'
		signal = 'bull'
		cur['pattern'] = pattern
		cur['signal'] = signal
	# Bearish Pinbar
	# if body <= (range / 3) and max(open, close) < (high + low) / 2 and current high > previous high
	# if the real body is smaller than a third of the range and the body is located in the lower half
	elif real_body <= (candle_range / 3) and max(cur['open'], cur['close']) < ((cur['high'] + cur['low']) / 2) and cur['high'] > prev['high']:
		pattern = 'bearish pinbar'
		signal = 'bear'
		cur['pattern'] = pattern
		cur['signal'] = signal
	# Bullish Engulfing
	# if current high > previous high and current low < previous low and real body >= 80% of range and current close > current open
	elif cur['high'] > prev['high'] and cur['low'] < prev['low'] and real_body >= 0.8 * candle_range and cur['close'] > cur['open']:
		pattern = 'bullish engulfing'
		signal = 'bull'
		cur['pattern'] = pattern
		cur['signal'] = signal
	# Bearish Engulfing
	# if current high > previous high and current low < previous low and real body >= 80% of range and current close < current open
	elif cur['high'] > prev['high'] and cur['low'] < prev['low'] and real_body >= 0.8 * candle_range and cur['close'] < cur['open']:
		pattern = 'bearish engulfing'
		signal = 'bear'
		cur['pattern'] = pattern
		cur['signal'] = signal
	else:
		cur['pattern'] = ''
		cur['signal'] = ''
	return cur


class PatternRecognition:

	def __init__(self, candles):
		self.candles = candles

	def scan_pattern(self):
		cur = self.candles[2]
		prev = self.candles[1]
		prev2 = self.candles[0]
		return patterns(cur, prev, prev2)

	def scan_patterns_historical(self):
		for i in range(2, len(self.candles)):
			cur = self.candles[i]
			prev = self.candles[i-1]
			prev2 = self.candles[i-2]
			self.candles[i] = patterns(cur, prev, prev2)
		self.candles[0]['pattern'] = ''
		self.candles[0]['signal'] = ''
		self.candles[1]['pattern'] = ''
		self.candles[1]['signal'] = ''
		return self.candles
