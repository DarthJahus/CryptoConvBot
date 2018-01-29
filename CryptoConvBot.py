# coding=utf-8
# CryptoConvBot 2

import logging
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, utils
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, Filters, MessageHandler
from Converter import convert, api_convert_coin
from emoji import emojize
import HelperFunctions as Helper
import api_coinmarketcap
import urllib3
urllib3.disable_warnings()


# Config
dev = "jahus"  # ou mohus
__debug = True
config = Helper.load_file_json("config.json")

# VARIABLES
__version__ = "2.1814"
__bot_name = "CryptoConvBot"
__DONATION_ETH = "0x624688e4012c9E6Be7239BeA0A575F8e41B4B3B6"
__DONATION_XVG = "DCY3HQXo8JtTGomK1673QgT4rkX8rdyZXA"
__DONATION_PND = "PEwzKUUf1noKQaSkzKinPZ6irJBL1WckB4"
__DONATION_BTC = "1EnQoCTGBgeQfDKqEWzyQLaKWQbP2YR1uU"

# CONSTANTS
__help = {
	"fr":
		"*HELP* %s\n\n*Conversion :*\n/convert amount coin1 coin2\n::` /convert 1 ETH USD`"
		"\n\n*Get ticker :*\n/ticker coin\n::`  /ticker BCH`\n\n*Get snapshot of coin :*\n/snap coin\n::`  /snap ETH`"
		"\n\n*INLINE MODE* %s\n"
		"This bot can bot used in inline mode to convert, just write :\n"
		"`@CryptoConvBot`"
		% (emojize(":key:"), emojize(":arrow_right_hook:", use_aliases=True))
}
__ABOUT_TEXT = \
	"*CryptoConBot v %s*\nby %s @Jahus, %s @mohus, %s @foudre.\n\nSend /help to see how it works :\n\n" \
	"*DONATIONS*\nIf you like our work, you can donate %s\n" \
	"*ETH/ETC:* `%s`\n" \
	"*XVG:* `%s`\n" \
	"*PND:* `%s`\n" \
	"*BTC/BCH:* `%s`\n" \
	"Thanks !\n\n*Credits* :\n" \
	"API from [CryptoCoinMarket](https://coinmarketcap.com)\n" \
	"API from [Cryptonator](https://www.cryptonator.com)" \
	% (
		__version__, emojize(':robot_face:'), emojize(':alien_monster:'), emojize(':alien:'),
		emojize(':beers:', use_aliases=True), __DONATION_ETH, __DONATION_XVG, __DONATION_PND, __DONATION_BTC
	)
__thumb_url = {
	"CryptoCompare": {
		"url": "https://i.imgur.com/LAOOxhM.png",
		"width": 64,
		"height": 64
	},
	"Cryptonator": {
		"url": "https://i.imgur.com/SoeT9GX.png",
		"width": 64,
		"height": 64
	},
	"error": {
		"url": "https://i.imgur.com/vyxEwc9.png",
		"width": 64,
		"height": 64
	}
}

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.CRITICAL
)
logger = logging.getLogger(__name__)


# Define a dew command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def cmd_start(bot, update):
	"""Send a message when the command /start is issued."""
	update.message.reply_text('Hi !\nUse /help to see how I can help you.')


def cmd_about(bot, update):
	"""Send a message when the command /start is issued."""

	if update.effective_chat.type == "private":
		update.message.reply_text(
			__ABOUT_TEXT,
			quote=True,
			parse_mode=ParseMode.MARKDOWN,
			disable_web_page_preview=True
		)
	else:
		update.message.reply_text(
			"You can't ask this in public ! %s\nPlease [click here](https://telegram.me/%s?start=about)."
			% (emojize(":nerd_face:"), __bot_name),
			quote=True,
			parse_mode=ParseMode.MARKDOWN,
			disable_web_page_preview=True,
		)


def cmd_convert(bot, update, args):
	update.message.reply_text(convert(args), parse_mode=ParseMode.MARKDOWN, quote=True)


def cmd_ticker(bot, update, args):
	update.message.reply_text(convert([args[0], "btc"]), parse_mode=ParseMode.MARKDOWN, quote=True)


def inline_query(bot, update):
	query = update.inline_query.query

	if not query:
		return

	# on obtient les résultats de tous les exchanges (-query- contient la commande)
	# query est transformé en liste pour être décodé comme -args-
	convertion_results = api_convert_coin(query.split(), inline_call=True)

	# elle contiendra la liste des "articles" inline à afficher
	results = list()

	if not convertion_results["success"]:
		results.append(
			InlineQueryResultArticle(
				id="%s/-1" % update.inline_query.id,
				title="Conversion error",
				input_message_content=InputTextMessageContent(
					"*Error :(*\nFailed to convert \"`%s`\". Sorry.\n%s" % (convertion_results["result"], query),
					parse_mode=ParseMode.MARKDOWN
				),
				description="Failed to convert. Sorry.\n%s" % convertion_results["result"],
				thumb_url=__thumb_url["error"]["url"],
				thumb_height=__thumb_url["error"]["height"],
				thumb_width=__thumb_url["error"]["width"]
				)
			)
	else:
		_res_id = 0
		for service in convertion_results["result"]:
			results.append(
				InlineQueryResultArticle(
					id="%s/%s" % (update.inline_query.id, _res_id),
					title=service,
					input_message_content=InputTextMessageContent(
						message_text=convertion_results['result'][service],
						parse_mode=ParseMode.MARKDOWN
					),
					description=convertion_results['result_inline'][service],
					thumb_url=__thumb_url[service]["url"],
					thumb_width=__thumb_url[service]["width"],
					thumb_height=__thumb_url[service]["height"]
				)
			)
			_res_id+=1
	update.inline_query.answer(results)


def cmd_snap(bot, update, args):
	if len(args) > 1:
		# trop d'argument
		update.message.reply_text(
			"*Error :(*\n"
			"*Usage :* `/snap <coin0>`\n",
			parse_mode="Markdown"
		)
	else:
		# USD par défaut
		_unit_source = args[0].lower()
		_unit_target = "usd"
		results = api_coinmarketcap.get_snap(_unit_source, _unit_target)
		# Check the results
		if results["success"]:
			# Emoji +/-
			if results["result"]["change24"][0] == '-':
				_change_sign = emojize(":small_red_triangle_down:", use_aliases=True)
			else:
				_change_sign = emojize(":small_red_triangle:", use_aliases=True)
			# Retour
			update.message.reply_text(
				"*%s* (%s)\n\n*Price:* `%s USD | %s BTC`\n*Change 24h:* `%s%%` %s\n*Vol. 24h:* `%s USD`\n*MarketCap:* `%s USD`" \
				% (
					args[0].upper(), results["result"]["coin_name"],
					results["result"]["price_usd"],
					results["result"]["price_btc"],
					results["result"]["change24"],
					_change_sign, # utils.helpers.escape_markdown(_change_sign),
					results["result"]["24volume_usd"],
					results["result"]["market_cap_usd"]
				),
				parse_mode=ParseMode.MARKDOWN
			)
		else:
			update.message.reply_text("*Error :(*\n%s" % results["message"], parse_mode=ParseMode.MARKDOWN)


def cmd_easter_egg(bot, update):
	update.message.reply_photo("https://i.imgur.com/gzjl0yD.jpg")


def cmd_help(bot, update):
	"""Send a message when the command /help is issued."""
	update.message.reply_text(__help["fr"], parse_mode=ParseMode.MARKDOWN, quote=True)


def event_group_join(bot, update):
	"""Reply when a member joins the group."""
	msg = update.message
	# si le nouvel utilisateur est un bot, on ne dit rien
	# ***à débattre !!
	if msg.new_chat_member.is_bot:
		update.message.reply_text(
			"`0x48656C6C6F2C20%s21`" % msg.new_chat_member.username.encode("hex").upper(),
			parse_mode=ParseMode.MARKDOWN,
			quote=True
		)
	else:
		update.message.reply_text("Hello, %s." % msg.new_chat_member.first_name, quote=True)


def event_group_leave(bot, update):
	"""Reply when a member leaves the group."""
	msg = update.message
	if not msg.new_chat_member.is_bot:
		update.message.reply_text("Bye, %s." % msg.left_chat_member.username, quote=True)


def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)


def main():
	"""Start the bot."""
	# Create the EventHandler and pass it your bot's token.
	updater = Updater(config["token"][dev])

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", cmd_start))
	dp.add_handler(CommandHandler("help", cmd_help))
	dp.add_handler(CommandHandler("about", cmd_about))
	dp.add_handler(CommandHandler("convert", cmd_convert, pass_args=True))
	dp.add_handler(InlineQueryHandler(inline_query))
	dp.add_handler(CommandHandler("snap", cmd_snap, pass_args=True))
	dp.add_handler(CommandHandler("ticker", cmd_ticker, pass_args=True))
	dp.add_handler(CommandHandler("keskifichou", cmd_easter_egg))

	# quand quelqu'un rejoint/quitte le chat
	dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, event_group_join))
	dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, event_group_leave))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

	# Generate a coin list from CoinMarketCap
	if not __debug: api_coinmarketcap.generate_cmc_coinlist()


if __name__ == '__main__':
	main()
