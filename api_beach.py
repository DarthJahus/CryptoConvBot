# coding=utf-8
import requests
import time
import helperfunctions as Helper


# Cache management
__time_sync = 0
__instantCoinList = []
__sync_delay = 60*60


# charge le fichier en cache; s'il ne l'est pas (To-Do: Mettre un Time-out, pour resync)
# et identifie l'id de la monnaie depuis le symbol envoyé en args
def get_cmc_symbol(args):
	# si le temps correspond à la valeur originelle de la variable
	# il s'agit probablement du premier lancement, donc on obtient la liste
	# on la sauvegarde, et on obtient la liste id/symbol
	# qui est elle même mise en cache
	global __time_sync, __instantCoinList # Si on modifie une variable globale à l'intérieur d'une fonction, il faut la déclarer.
	if __time_sync + __sync_delay <= time.time():
		generate_cmc_coinlist()
		coinlist = Helper.load_file_json("cryptomarketcap_list.json")
		__instantCoinList = coinlist
		# on met la dernière fois qu'on a syncé à maintenant (now)
		__time_sync = time.time()
		return __instantCoinList[args][0]
	else:
		# Comme on a quelque chose en cache, on la charge directement
		return __instantCoinList[args][0]


# obtient la liste des monnaies depuis le site, et enregistre en local la liste (id/symbole)
def generate_cmc_coinlist():
	try:
		req = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0") # limit 0 : liste toutes les monnaies
		coinlist_tosave = {}
		if len(req.json()) != 0:
			for money in req.json():
				coinlist_tosave[money["symbol"]]=[money["id"]]
			# enregistrement de la liste des monnaies dispos
			# cache/optimisation :D :D
			Helper.save_file_json('cryptomarketcap_list.json',coinlist_tosave)
	except:
		return {"success": False, "error": "Error from api_cryptomarketcap [list]"}


def api_coinmarketcap_get_snap(coin_0, coin_1):
	try:
		# on prend le symbole de la monnaie depuis la liste
		# monnaie envoyée en arg en majuscules
		_coin_0 = get_cmc_symbol(coin_0.upper())
		req = requests.get("https://api.coinmarketcap.com/v1/ticker/%s/?convert=%s" % (_coin_0, coin_1.upper()))
		if req.status_code != 200:
			return {"success": False, "message": "Received error %s from CoinMarketCap" % req.status_code}
		else:
			req_dict=req.json()
			_change24h = req_dict[0]['percent_change_24h']
			_change7d = req_dict[0]['percent_change_7d']
			_volume24h_USD = req_dict[0]['24h_volume_usd']
			_price_USD = req_dict[0]['price_usd']
			_price_BTC = req_dict[0]['price_btc']
			_market_cap_usd = req_dict[0]["market_cap_usd"]
			return {
				"success": True,
				"result": {
					"price_usd": _price_USD,
					"price_btc": _price_BTC,
					"change24" : _change24h,
					"change7d" : _change7d,
					"coin_name" : _coin_0,
					"24volume_usd" : "{:,.0f}".format(float(_volume24h_USD)).replace(',', ' '),
					"market_cap_usd": "{:,.0f}".format(float(_market_cap_usd)).replace(',', ' ')
				}
			}
	except:
		return {"success": False, "message": "Error from api_coinmarketcap_get_snap()"}
