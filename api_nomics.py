import requests

__API_KEY = "76f9652f975e291d830006ee5d5c4126" # Unlimited calls (works from localhost/127.0.0.1/0.0.0.0 or a domain to spectify to Nomics)


def get_nomics_convert(coin1, coin2):
    try:
        url_ticker = "https://api.nomics.com/v1/currencies/ticker?key=%s&ids=%s&interval=1h&convert=%s" % (__API_KEY, coin1, coin2)
        _price = float(requests.get(url_ticker).json()[0]['price'])
        return {
					"success": True,
					"result": {
						"last": _price,
						"sell": _price,
						"buy": _price
					},
					"exchange": "Nomics",
					"pair": [coin1, coin2]
				}
    except:
        return {"success": False, "message": "Error from api_nomic_ticker()"}
