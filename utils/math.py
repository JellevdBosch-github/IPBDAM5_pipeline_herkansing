import math
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def convert_currency(base, to, amount):
	"""
	Converts a currency to target currency
	:param base: Currency to be converted
	:param to: Currency to get the conversion result from
	:param amount: The amount to be converted
	:return: Float: Price of the amount to be converted
	"""
	url = ' https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
	parameters = {
		'symbol': base,
		'convert': to,
		'amount': amount
	}

	# too lazy to secure key
	# 57e78373-0c60-4f4c-aa10-966bd4c9b970

	# Set headers, including API key
	headers = {
		'Accepts': 'application/json',
		'X-CMC_PRO_API_KEY': '57e78373-0c60-4f4c-aa10-966bd4c9b970',
	}
	session = Session()
	session.headers.update(headers)

	# Get and return the data
	try:
		response = session.get(url, params=parameters)
		data = json.loads(response.text)
		return data['data']['quote'][to]['price']
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)


def get_integer_places(n):
	"""
	Calculates the amount of places of an integer using log10() of the math module.
	:param n: Integer: The number of which the amount of digits will be calculated.
	:return: Integer: The amount of digits the parameter number contains.
	Requires an integer.

	Another, but slower option is to use: len(str())

	IMPORTANT: Gives problems when the number is greater than 999999999999997 (15 places).
	The float then has too many 9sm causing the result to round up.
	Therefore a check is executed to check whether the absolute value of the parameter is not greater than that,
	consequently not adding up a '1'.
	"""
	if n != 0:
		if abs(n) <= 999999999999997:
			return int(math.log10(abs(n))) + 1
		else:
			return int(math.log10(abs(n)))
	else:
		return 1
