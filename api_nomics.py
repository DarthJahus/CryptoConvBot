import requests
import time

__API_KEY = "76f9652f975e291d830006ee5d5c4126" # Unlimited calls (works from localhost/127.0.0.1/0.0.0.0 or a domain to spectify to Nomics)

global tokens_prices
tokens_prices = dict()

def get_nomics_prices():
    try:
        url_ticker = "https://api.nomics.com/v1/currencies/ticker?key=%s&interval=1h,1d,7d&convert=USD" % (__API_KEY)
        result = requests.get(url_ticker).json()

        print("API Nomics requested")

        """

            TOKEN_NAME
                PRICE               //
                1H-PRICE            // 
                1D-PRICE            // DATA
                7H-PRICE            // 
                MARKET-CAP          //

            ['TOKEN_NAME', '[DATA]']

        """

        for item in result:

            tk_name         = item["id"]
            tk_price        = (item["price"])
            tk_1hprice      = "%.2f" % (float(item["1h"]["price_change_pct"])  * 100) # tout en str pour pas se faire chier
            tk_1dprice      = "%.2f" % (float(item["1d"]["price_change_pct"])  * 100) # après avec des %f des %s et autres
            tk_7dprice      = "%.2f" % (float(item["7d"]["price_change_pct"])  * 100) # sinon, changer put_sign(), et get_coin_price()
            tk_marketcap    = float(item["market_cap"])
                
            tokens_prices[tk_name] =  {
                    "price"         : tk_price,
                    "1h-price-ch"   : tk_1hprice,
                    "1d-price-ch"   : tk_1dprice,
                    "7d-price-ch"   : tk_7dprice,
                    "market-cap"    : tk_marketcap
            }

            tokens_prices["last_timestamp"] = time.time()

    except Exception as e:
        return {"success": False, "message": "Error from api_nomics_ticker()"}

def format_price(price):
    price=float(price)
    if price < 1:
        return "%.8f" % price
    elif price < 10000:
        return "%.4f" % price
    elif price >= 10000:
        return "%.2f" % price

def format_thousands(price):
    return f"{price:,}"

def put_sign(price):
    price_trend = ["\U0001F539", "\U0001F53B"] # up - down 	
    # number length 7 : +000.00  
    if price[0]=="-":
        n_spaces = (7 - len(price))*(" ")
        return price + n_spaces + price_trend[1] # down
    else:
        n_spaces = (6 - len(price))*(" ")
        return "+" + price+ n_spaces + price_trend[0] # up

def get_coin_price(coin):
    if "last_timestamp" in tokens_prices:
        if time.time()-tokens_prices["last_timestamp"]>=59:
            get_nomics_prices()
        else:
            pass
    else:
        get_nomics_prices()
    
    coin = coin.upper()

    _message = "*>> %s - USD*\n*Price* : `%s` USD.\n*1H Price change* : `%s`\n*1D Price change* : `%s`\n*7D Price change* : `%s`\n*Market cap.* : `%s` USD." % (
        coin, format_price(tokens_prices[coin]["price"]), 
        put_sign(tokens_prices[coin]["1h-price-ch"]), 
        put_sign(tokens_prices[coin]["1d-price-ch"]), 
        put_sign(tokens_prices[coin]["7d-price-ch"]), 
        format_thousands(tokens_prices[coin]["market-cap"])
    )

    return _message