# coding=utf-8
# Fork de CryptoConvBot v1 de @Jahus
# Version 2 par @Mohus
# -----------------------------

import requests
import emoji
import urllib3


urllib3.disable_warnings()


# consts
units = {
	"btc": {
		"name": "Bitcoin",
		"short": "BTC",
		"submultiple": "SAT",
		"multiplier": 1e+8
	},
	"ltc": {
		"name": "Litcoin",
		"short": "LTC",
		"submultiple": "LIT",
		"multiplier": 1e+8
	}
}


#  APIs de conversion
def api_cryptonator(coin_0, coin_1):
	try:
		_exchange = "Cryptonator"
		req = requests.get("https://www.cryptonator.com/api/ticker/%s-%s" % (coin_0, coin_1))
		if req.status_code != 200:
			return {"success": False, "error": ("Error %s from Cryptonator" % req.status_code)}
		else:
			req_dict = req.json()
			if not req_dict["success"]:
				return {"success": False, "error": ("Error from Cryptonator: %s" % req_dict["error"])}
			else:
				_last = float(req_dict["ticker"]["price"])
				_sell = _last
				_buy = _last
				return {
					"success": True,
					"result": {
						"last": _last,
						"sell": _sell,
						"buy": _buy
					},
					"exchange": _exchange,
					"pair": [req_dict["ticker"]["base"], req_dict["ticker"]["target"]]
				}
	except:
		return {"success": False, "error": "Error from api_cryptonator()"}


def api_cryptocompare(coin_0, coin_1):
	try:
		_exchange = "CryptoCompare"
		req = requests.get("https://min-api.cryptocompare.com/data/price?fsym=%s&tsyms=%s" % (coin_0, coin_1))
		if req.status_code != 200:
			return {"success": False, "error": ("Error %s from CryptoCompare" % req.status_code)}
		else:
			req_dict = req.json()
			if "Response" in req_dict:
				return {"success": False, "error": ("Error from CryptoCompare: %s" % req_dict["Message"])}
			else:
				_last = float(req_dict[coin_1.upper()])
				_sell = _last
				_buy = _last
				return {
					"success": True,
					"result": {
						"last": _last,
						"sell": _sell,
						"buy": _buy
					},
					"exchange": _exchange,
					"pair": [coin_0.upper(), coin_1.upper()]
				}
	except:
		return {"success": False, "error": "Error from api_cryptocompare()"}


def api_convert_coin(args, inline_call):
	if len(args) > 3 or len(args) < 2:
		return {"success": False, "result": ""}
	else:
		_value = 1.
		sources = []

		# Calling API
		if len(args) == 3:
			try:
				_value = float(args[0])
				print("** api_convert_coin(): value = %.8f" % _value)
			except:
				print("** api_convert_coin(): Error while trying to get the value of args[0] (args[0] = %s)" % args[0])
		try:
			if len(args) == 3:
				sources.append(api_cryptocompare(args[1].upper(), args[2].upper()))
				sources.append(api_cryptonator(args[1].upper(), args[2].upper()))
			else:
				# len(args) == 2
				sources.append(api_cryptocompare(args[0].upper(), args[1].upper()))
				sources.append(api_cryptonator(args[0].upper(), args[1].upper()))
		except:
			print("** Error from api_convert_coin() while trying to use API function.")

		# Parse info
		_results = {}
		_results_inline = {}
		_success = False
		for source in sources:
			if not source["success"]:
				print("** api_convert_coin():\n\t%s" % source["error"])
			else:
				_price = float(source["result"]["last"]) * _value

				if len(args) == 3:
					_unit_source = args[1].upper()
					_unit_target = args[2].upper()
				else:
					_unit_source = args[0].upper()
					_unit_target = args[1].upper()
				# Check if source unit and value can be simplified
				if (_unit_source.lower() in units) and (_value < 0.00001):
					_unit_source = "%s %s"\
						% (
							int(_value * units[_unit_source.lower()]["multiplier"]),
							units[_unit_source.lower()]["submultiple"]
						)
				else:
					if _value < 0.001:
						_unit_source = "%.8f %s" % (_value, _unit_source)
					else:
						if _value - int(_value) == 0:
							_unit_source = "%i %s" % (int(_value), _unit_source)
						else:
							_unit_source = "%.4f %s" % (_value, _unit_source)
						
				if (_unit_target.lower() in units) and (_price < 0.00001):
					_price = int(_price * units[_unit_target.lower()]["multiplier"])
					_unit_target = units[_unit_target.lower()]["submultiple"]
				else:
					if _price < 0.001:
						_price = "%.8f" % _price
					else:
						if _price - int(_price) == 0:
							_price = "%i" % int(_price)
						else:
							_price = "%.4f" % _price

				# Answer message body
				_results[source["exchange"]] = "%s %s\n`%s = %s %s`"\
					% (
						emoji.emojize(':white_small_square:'),
						source["exchange"],
						_unit_source,
						_price,
						_unit_target
					)
				# Description for inline elements
				if inline_call:
					_message_inline = "%s = %s %s" % (_unit_source, _price, _unit_target)
					_results_inline[source["exchange"]] = _message_inline
				_success = True

		# Check if any API call has been successful
		if _success:
			if inline_call:
				return {"success": True, "result": _results, "result_inline": _results_inline}
			else:
				return {"success": True, "result": _results}
		else:
			return {"success": False, "result": "All sources returned an error."}


def convert(args):
	"""
	Provide 2 or 3 args
	And perform len(args) check BEFORE calling this function.
	"""
	results_tmp = api_convert_coin(args, inline_call=False)
	results = []
	if not results_tmp["success"]:
		results.append("*Error :(*\n_%s_\nFailed to convert. Sorry." % results_tmp["result"])
	else:
		for service in results_tmp["result"]:
			results.append(results_tmp["result"][service])
	return '\n'.join(results)
