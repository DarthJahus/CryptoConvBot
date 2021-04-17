from emoji import emojize


# VARIABLES
__version__ = "4.5 (2020-02-28)"
__bot_name = "CryptoConvBot"
__DONATION_ETH = "0x624688e4012c9E6Be7239BeA0A575F8e41B4B3B6"
__DONATION_XLM = "GDRG4SI4GT6YUIOVOBBCTQGZOUYVGRN534CQU4NX76KGPGQ7MS4ZM4EI"
__DONATION_BTC = "1EnQoCTGBgeQfDKqEWzyQLaKWQbP2YR1uU"

# consts
__help = {
	"en":
		"*HELP* %s\n\n"
		"[Check the Wiki for detailed help](https://github.com/DarthJahus/CryptoConvBot/wiki)\n\n"
		"*%s Conversion:*\n`/convert [amount] <coin1> <coin2>`\n::` /convert ETH USD`\n::` /convert 3 ETC USD`"
		"\n\n*%s Price:*\n`/price <coin>`\n::` /price DOT`"
		"\n\n%s *Inline mode:*\nYou can summon me from any chat by writing `@CryptoConvBot`."
		"\n:: `@CryptoConvBot DOGE BTC`\n:: `@CryptoConvBot 5 NEO EUR`"
		"\n\n%s *Any question or suggestion?*\nContact @Jahus"
		"\n\n%s Use /about to learn more about me and my creators."
		% (
			emojize(":key:", use_aliases=True),
			emojize(":arrows_counterclockwise:", use_aliases=True),
			emojize(":eyes:", use_aliases=True),
			emojize(":arrow_right_hook:", use_aliases=True),
			emojize(":nerd_face:", use_aliases=True),
			emojize(":information_source:", use_aliases=True)
		)
}


__advertisements = {
	"nord_vpn": {
		"message": "Secure your connection with NordVPN.",
		"rate": 1,
		"emoji": ":earth_americas:",
		"url": "https://bit.ly/CCNordVPN"
	},
	"ai_marketing": {
		"message": "Get $50 cash on ai.marketing.",
		"rate": 22,
		"emoji": ":robot:",
		"url": "https://bit.ly/AIMarketing50"
	},
	"binance_20": {
		"message": "Trade crypto on Binance",
		"rate": 25,
		"emoji": ":money_bag:",
		"url": "https://bit.ly/BinanceMohus"
	},
	"binance_15": {
		"message": "Trade crypto on Binance (+bonus)",
		"rate": 15,
		"emoji": ":money_bag:",
		"url" : "https://bit.ly/BinanceMohus15"
	},
	"ledger_nano_s": {
		"message": "Secure your coins: Use Ledger Nano S.",
		"rate": 5,
		"emoji": ":credit_card:",
		"url": "https://bit.ly/LedgerNanoSJahus"
	},
	"ledger_nano_x": {
		"rate": 0,
		"emoji": ":credit_card:",
		"message": "Hold your crypto securly. Use Ledger Nano X.",
		"url": "https://bit.ly/LedgerNanoXJahus"
	},
	"about": {
		"rate": 0,
		"emoji": ":coffee:",
		"message": "Buy me a coffee!",
		"url": "https://telegram.me/%s?start=about" % __bot_name
	},
	"nothing": {
		"rate": 5,
		"message": None
	},
	"discord": {
		"rate": 20,
		"emoji": ":confetti_ball:",
		"message": "Add me on Discord!",
		"url": "http://bit.ly/CryptoConvBotGraph"
	},
	"free_bitcoin": {
		"rate": 22,
		"emoji": ":money_bag:",
		"message": "The best Bitcoin faucet.",
		"url": "http://bit.ly/CCFreeBTC"
	}
}

__ABOUT_TEXT = (
		"*CryptoConBot ver. %s*\nBy %s @Jahus, %s @Mohus."
		"\n\n%s Send /help to see how it works."
		"\n\n%s *Donations*"
		"\n- *ETH/ETC:* `%s`"
		"\n- *XLM:* `%s`"
		"\n- *BCH/BTC:* `%s`"
		"\nThank you!"
		"\n\n%s *Credits*"
		"\n- API from [CryptoCoinMarket](https://coinmarketcap.com)"
		"\n- API from [Cryptonator](https://www.cryptonator.com)"
	) % (
		__version__, emojize(':robot_face:'), emojize(':alien_monster:'),
		emojize(":key:", use_aliases=True),
		emojize(':coffee:', use_aliases=True),
		__DONATION_ETH,
		__DONATION_XLM,
		__DONATION_BTC,
		emojize(":linked_paperclips:", use_aliases=True)
	)

__thumb_url = {
	"Cryptonator": {
		"url": "https://i.imgur.com/4Shr41n.png",
		"width": 64,
		"height": 64
	},
	"CryptoCompare": {
		"url": "https://i.imgur.com/FWEOyTT.png",
		"width": 64,
		"height": 64
	},
	"error": {
		"url": "https://i.imgur.com/AWeJubR.png",
		"width": 64,
		"height": 64
	}
}
