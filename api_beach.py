import requests
from helperfunctions import load_file_json
from helperfunctions import save_file_json

def getCMC_symbol(args):
	coinlist = load_file_json("cryptomarketcap_list.json")
	return coinlist[args]

def generate_CMC_coinlist():
	try:
		req = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0")
		coinlist_tosave = {}
		if len(req.json()) != 0:
			for money in req.json():
				coinlist_tosave[money["symbol"]]=[money["id"]]
			# enregistrement de la liste des monnaies dispos
			# cache/optimisation :D
			save_file_json('cryptomarketcap_list.json',coinlist_tosave)
	except:
		return {"success": False, "error": "Error from api_cryptomarketcap [list]"}

def api_coinmarketcap_getSnap(coin_0, coin_1):
	try:
		# on prend le symbole de la monnaie depuis la liste
		__coin_0 = getCMC_symbol(coin_0)
		print "https://api.coinmarketcap.com/v1/ticker/%s/?convert=%s" % (str(__coin_0), coin_1)
		req = requests.get("https://api.coinmarketcap.com/v1/ticker/%s/?convert=%s" % (__coin_0, coin_1))
		if (req.status_code != 200):
			return {"success": False, "error": ("Error %s from CryptoCompare" % req.status_code)}
		else:
			req_dict=req.json()
			if (req_dict["success"] != True):
				return {"success": False, "error": ("Error from CryptCompare: %s" % req_dict["error"])}
			else:
				_change24h = req_dict['percent_change_24h']
				_change7d = req_dict['percent_change_7d']
				_volume24h_USD = req_dict['2h_volume_usd']
				return {"success": True,
						"result":{"change24" : _change24h, "change7d" : _change7d, "24volume_usd" : _volume24h_USD}}

	except:
		return {"success": False, "error": "Error from api_cryptocompare [snap]"}
