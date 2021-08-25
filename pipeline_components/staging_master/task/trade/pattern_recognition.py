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
	real_body = abs(cur[1] - cur[4])
	# high - low
	candle_range = cur[2] - cur[3]


	# Bullish Swing
	# if current low > previous low and previous low < previous2 low
	if cur[3] > prev[3] and prev[3] < prev2[3]:
		pattern = 'bullish swing'
		signal = 'bull'
		cur.append(pattern)
		cur.append(signal)
	# Bearish Swing
	# if current high < previous high and previous high > previous2 high
	elif cur[2] < prev[2] and prev[2] > prev2[2]:
		pattern = 'bearish swing'
		signal = 'bear'
		cur.append(pattern)
		cur.append(signal)
	# Bullish Pinbar
	# if body <= (range / 3) and min(open, close) > (high + low) / 2 and current low < previous low
	# if the real body is smaller than a third of the range and the body is located in the upper half
	elif real_body <= (candle_range / 3) and min(cur[1], cur[4]) > ((cur[2] + cur[3]) / 2) and cur[3] < prev[3]:
		pattern = 'bullish pinbar'
		signal = 'bull'
		cur.append(pattern)
		cur.append(signal)
	# Bearish Pinbar
	# if body <= (range / 3) and max(open, close) < (high + low) / 2 and current high > previous high
	# if the real body is smaller than a third of the range and the body is located in the lower half
	elif real_body <= (candle_range / 3) and max(cur[1], cur[4]) < ((cur[2] + cur[3]) / 2) and cur[2] > prev[2]:
		pattern = 'bearish pinbar'
		signal = 'bear'
		cur.append(pattern)
		cur.append(signal)
	# Bullish Engulfing
	# if current high > previous high and current low < previous low and real body >= 80% of range and current close > current open
	elif cur[2] > prev[2] and cur[3] < prev[3] and real_body >= 0.8 * candle_range and cur[4] > cur[1]:
		pattern = 'bullish engulfing'
		signal = 'bull'
		cur.append(pattern)
		cur.append(signal)
	# Bearish Engulfing
	# if current high > previous high and current low < previous low and real body >= 80% of range and current close < current open
	elif cur[2] > prev[2] and cur[3] < prev[3] and real_body >= 0.8 * candle_range and cur[4] < cur[1]:
		pattern = 'bearish engulfing'
		signal = 'bear'
		cur.append(pattern)
		cur.append(signal)
	else:
		cur.append('')
		cur.append('')
	return cur


class PatternRecognition:

	def __init__(self, candles):
		self.candles = candles

	def scan_pattern(self):
		cur = self.candles[0]
		prev = self.candles[1]
		prev2 = self.candles[2]
		return patterns(cur, prev, prev2)

	def scan_patterns_historical(self):
		for i in range(2, len(self.candles)):
			cur = self.candles[i]
			prev = self.candles[i-1]
			prev2 = self.candles[i-2]
			self.candles[i] = patterns(cur, prev, prev2)

	def get_candles(self):
		return self.candles
