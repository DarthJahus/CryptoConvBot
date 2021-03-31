import requests
import time
import helperfunctions as Helper

__API_KEY = "76f9652f975e291d830006ee5d5c4126"  # Unlimited calls (works from localhost/127.0.0.1/0.0.0.0 or a domain to spectify to Nomics)


tokens_prices = {}
_data_timestamp = -1
price_trend = ["󠀽\U000025AB", "\U0001F539", "\U0001F53B"]  # equal - up - down


def get_nomics_prices():
    global _data_timestamp
    _url_ticker = "https://api.nomics.com/v1/currencies/ticker?key=%s&interval=1h,1d,7d&convert=USD" % __API_KEY
    _req = requests.get(_url_ticker)
    if _req.status_code != 200:
        return {"success": False, "message": "Nomics API returned error %i" % _req.status_code}
    else:
        _req_json = _req.json()
        try:
            for item in _req_json:
                tokens_prices[item["id"].upper()] = {
                    "price": float(item["price"]),
                    "1h-price-ch": float(item["1h"]["price_change_pct"]) * 100,  # tout en str pour pas se faire chier,
                    "1d-price-ch": float(item["1d"]["price_change_pct"]) * 100,  # après avec des %f des %s et autres,
                    "7d-price-ch": float(item["7d"]["price_change_pct"]) * 100,  # sinon, changer put_sign(), et get_coin_price(),
                    "market-cap": float(item["market_cap"])
                }
            _data_timestamp = time.time()
        except KeyError:
            return {"success": False, "message": "Got unexpected data form Nomics API."}


def format_price(price):
    if price < 10:
        return "%.8f" % price
    elif price < 1000:
        return "%.4f" % price
    elif price >= 1000:
        return "%.2f" % price


def sign(value):
    if value < 0:
        return -1
    if value > 0:
        return 1
    return 0


def get_coin_price(coin, raw=False, price_trend=price_trend):
    if time.time() - _data_timestamp > 60:
        _update = get_nomics_prices()
        if not _update["success"]:
            Helper.log_("Nomics", 0, 0, _update["message"])

    coin = coin.upper()

    if coin not in tokens_prices:
        return "Error: Can't find price for *%s*" % coin
    if raw:
        return {
            "Price": "`%s`" % format_price(tokens_prices[coin]["price"]),
            "1h change": "{} `{:=+7.2f}%`".format(price_trend[sign(tokens_prices[coin]["1h-price-ch"])], tokens_prices[coin]["1h-price-ch"]),
            "1d change": "{} `{:=+7.2f}%`".format(price_trend[sign(tokens_prices[coin]["1d-price-ch"])], tokens_prices[coin]["1d-price-ch"]),
            "7d change": "{} `{:=+7.2f}%`".format(price_trend[sign(tokens_prices[coin]["7d-price-ch"])], tokens_prices[coin]["7d-price-ch"]),
            "Market cap": f"`{tokens_prices[coin]['market-cap']:,}` `USD`"
        }
    else:
        _message = \
            "*>> %s - USD*\n\n" \
            "*Price*: `%s` `USD`.\n" \
            "*1h change*: %s%%\n" \
            "*1d change*: %s%%\n" \
            "*7d change*: %s%%\n" \
            "*Market cap.*: `%s` `USD`" % (
                coin,
                format_price(tokens_prices[coin]["price"]),
                "{} `{:=+7.2f}`".format(price_trend[sign(tokens_prices[coin]["1h-price-ch"])], tokens_prices[coin]["1h-price-ch"]),
                "{} `{:=+7.2f}`".format(price_trend[sign(tokens_prices[coin]["1d-price-ch"])], tokens_prices[coin]["1d-price-ch"]),
                "{} `{:=+7.2f}`".format(price_trend[sign(tokens_prices[coin]["7d-price-ch"])], tokens_prices[coin]["7d-price-ch"]),
                f"{tokens_prices[coin]['market-cap']:,}"
            )
        return _message
