#!/usr/bin/python3
# coding=utf-8

import logging
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, Filters, MessageHandler
from Converter import convert, api_convert_coin
from emoji import emojize
import helperfunctions as Helper
import api_coinmarketcap
import urllib3
urllib3.disable_warnings()
from datetime import datetime
import time
from random import choices


# Config
__dev = "mohus_test"  # "test" for tests, "bot" for production
__debug = False
config = Helper.load_file_json("config.json")

# VARIABLES
__version__ = "4.2 (2020-01-02)"
__bot_name = "CryptoConvBot"
__DONATION_ETH = "0x624688e4012c9E6Be7239BeA0A575F8e41B4B3B6"
__DONATION_XLM = "GDRG4SI4GT6YUIOVOBBCTQGZOUYVGRN534CQU4NX76KGPGQ7MS4ZM4EI"
__DONATION_BTC = "1EnQoCTGBgeQfDKqEWzyQLaKWQbP2YR1uU"

# CONSTANTS
__help = {
	"en":
		"*HELP* %s\n\n"
		"*%s Conversion:*\n`/convert [amount] <coin1> <coin2>`\n::` /convert ETH USD`\n::` /convert 3 ETC USD`"
		"\n\n*%s Ticker:*\n`/ticker <coin>`\n::` /ticker PND`"
		"\n\n*%s Snapshot of a coin:*\n`/snap <coin>`\n::` /snap BCH`"
		"\n\n%s *Inline mode:*\nYou can summon me from any chat by writing `@CryptoConvBot`."
		"\n:: `@CryptoConvBot DOGE BTC`\n:: `@CryptoConvBot 5 NEO EUR`"
	    "\n\n%s *Any question or suggestion?*\nContact @Jahus or @[censured]"
		"\n\n%s Use /about to learn more about me and my creators."
		% (
			emojize(":key:", use_aliases=True),
			emojize(":arrows_counterclockwise:", use_aliases=True),
			emojize(":eyes:", use_aliases=True),
			emojize(":chart_with_upwards_trend:", use_aliases=True),
			emojize(":arrow_right_hook:", use_aliases=True),
			emojize(":nerd_face:", use_aliases=True),
			emojize(":information_source:", use_aliases=True)
		)
}


__advertisements = {
	"binance_20": {
		"message": "Trade crypto on Binance",
		"rate": 25,
		"emoji": ":money_bag:",
		"url": "https://www.binance.com/en/register?ref=13980323"
	},
	"binance_15": {
		"message": "Trade crypto on Binance (get 5% on each transaction)",
		"rate": 20,
		"emoji": ":money_bag:",
		"url" : "https://www.binance.com/en/register?ref=PG8I2A3F"
	},
	"ledger_nano_s": {
		"message": "Secure your coins: Use Ledger Nano S.",
		"rate": 20,
		"emoji": ":credit_card:",
		"url": "https://shop.ledger.com/products/ledger-nano-s?r=aaad&tracker=cryptoconvbot"
	},
	"ledger_nano_x": {
		"rate": 5,
		"emoji": ":credit_card:",
		"message": "Hold your crypto securly. Use Ledger Nano X.",
		"url": "https://shop.ledger.com/pages/ledger-nano-x?r=aaad&tracker=cryptoconvbot"
	},
	"about": {
		"rate": 10,
		"emoji": ":coffee:",
		"message": "Buy me a coffee!",
		"url": "https://telegram.me/%s?start=about"
	},
	"nothing": {
		"rate": 20,
		"message": None
	}
}

__ABOUT_TEXT = (
		"*CryptoConBot ver. %s*\nBy %s @Jahus, %s @[censured]."
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
		emojize(':beers:', use_aliases=True),
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

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.ERROR #CRITICAL
)
logger = logging.getLogger(__name__)


def get_advertisement():
	_messages = []
	_rates = []
	for _item in __advertisements:
		if __advertisements[_item]["message"] is None:
			_messages.append("")
		else:
			_messages.append("\n\n%s [%s](%s)" % (emojize(__advertisements[_item]["emoji"], use_aliases=True), __advertisements[_item]["message"], __advertisements[_item]["url"]))
		_rates.append(__advertisements[_item]["rate"])
	print(sum(_rates))
	return choices(_messages, _rates)[0]


def cmd_about(bot, update):
	"""Send a message when the command /start is issued."""
	_cmd_name = "cmd_about"
	_result = None
	if update.effective_chat.type == "private":
		_result = "*msg__about"
		update.message.reply_text(
			__ABOUT_TEXT,
			quote=True,
			parse_mode=ParseMode.MARKDOWN,
			disable_web_page_preview=True
		)
	else:
		_result = "error__private_command_in_public"
		update.message.reply_text(
			"You can't ask this in public ! %s\nPlease [click here](https://telegram.me/%s?start=about)."
			% (emojize(":nerd_face:"), __bot_name),
			quote=True,
			parse_mode=ParseMode.MARKDOWN,
			disable_web_page_preview=True,
		)
	if _result is not None: Helper.log(_cmd_name, update, _result)


def cmd_convert(bot, update, args):
	_cmd_name = "cmd_convert"
	if len(args) in [2, 3]:
		_result = "[%s]" % ', '.join(args).replace('\n', '\\n')
		_message = convert(args) + get_advertisement()
	elif len(args) == 0:
		_result = None
		_message = None
	else:
		_result = "*error__invalid_query [%s]" % ", ".join(args).replace("\n", "\\n")
		_message = "Invalid query.\n[See help](https://t.me/cryptoconvbot?start=help)"
	if _result is not None:
		update.message.reply_text(_message, parse_mode=ParseMode.MARKDOWN, quote=True, disable_web_page_preview=True)
		Helper.log(_cmd_name, update, _result)


def cmd_ticker(bot, update, args):
	_cmd_name = "cmd_ticker"
	if len(args) == 1:
		_result = "[%s]" % ', '.join(args).replace('\n', '\\n')
		_message = convert([args[0], "btc"]) + get_advertisement()
	elif len(args) == 0:
		_result = None
		_message = None
	else:
		_result = "*error__invalid_query [%s]" % ", ".join(args).replace("\n", "\\n")
		_message = "Error: Invalid query:\n%s" % args
	if _result is not None:
		update.message.reply_text(_message, parse_mode=ParseMode.MARKDOWN, quote=True, disable_web_page_preview=True)
		Helper.log(_cmd_name, update, _result)


def cmd_price(bot, update, args):
	_cmd_name = "cmd_price"
	if len(args) == 1:
		_result = "[%s]" % ', '.join(args).replace('\n', '\\n')
		_message = convert([args[0], "usd"]) + get_advertisement()
	elif len(args) == 0:
		_result = None
		_message = None
	else:
		_result = "*error__invalid_query [%s]" % ", ".join(args).replace("\n", "\\n")
		_message = "Error: Invalid query:\n%s" % args
	if _result is not None:
		update.message.reply_text(_message, parse_mode=ParseMode.MARKDOWN, quote=True, disable_web_page_preview=True)
		Helper.log(_cmd_name, update, _result)


def inline_query(bot, update):
	_cmd_name = "inline"
	_result = None

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
		_result = "[%s]" % ', '.join(query.split()).replace('\n', '\\n')
	update.inline_query.answer(results)
	if _result is not None: Helper.log_(_cmd_name, update.effective_user.id, "{inline}", _result)


def cmd_snap(bot, update, args):
	_cmd_name = "cmd_snap"
	_result = None
	if len(args) > 1:
		# too many arguments
		_result = "*error__too_many_args"
		update.message.reply_text(
			"*Error :(*\n"
			"*Usage :* `/snap <coin0>`\n",
			parse_mode="Markdown"
		)
	else:
		# ETH by default, for @Seynon, USD is still retrieved
		_unit_source = args[0].lower()
		_unit_target = "eth"
		_results = api_coinmarketcap.get_snap(_unit_source, _unit_target)
		# Check the results
		if _results["success"]:
			# Emoji +/- for change on 24h
			if _results["result"]["change24"][0] == '-':
				_change_sign_24 = emojize(":small_red_triangle_down:", use_aliases=True)
			else:
				_change_sign_24 = emojize(":small_red_triangle:", use_aliases=True)
				_results["result"]["change24"] = "+" + _results["result"]["change24"]
			# Emoji +/- for change on 7d
			if _results["result"]["change7d"][0] == "-":
				_change_sign_7 = emojize(":small_red_triangle_down:", use_aliases=True)
			else:
				_change_sign_7 = emojize(":small_red_triangle:", use_aliases=True)
				_results["result"]["change7d"] = "+" + _results["result"]["change7d"]
			# Answer
			update.message.reply_text(
				"*%s* (%s)\n\n*Price:* `%s USD`\n`%s BTC | %s ETH`\n\n*Change 24 h:* `%s%%` %s\n*Change 7 d:* `%s%%` %s\n\n*Vol. 24 h:* `%s USD`\n*MarketCap:* `%s USD`" \
				% (
					args[0].upper(), _results["result"]["coin_name"],
					_results["result"]["price_usd"],
					_results["result"]["price_btc"],
					_results["result"]["price_eth"],
					_results["result"]["change24"],
					_change_sign_24, # utils.helpers.escape_markdown(_change_sign),
					_results["result"]["change7d"],
					_change_sign_7,
					_results["result"]["24volume_usd"],
					_results["result"]["market_cap_usd"]
				),
				parse_mode=ParseMode.MARKDOWN
			)
			_result = _unit_source
		else:
			_result = "*error__api_snap(%s)" % _unit_source
			update.message.reply_text("*Error :(*\n%s" % _results["message"], parse_mode=ParseMode.MARKDOWN)


def cmd_easter_egg(bot, update):
	update.message.reply_photo("https://i.imgur.com/gzjl0yD.jpg")


def cmd_help(bot, update):
	"""Send a message when the command /help is issued."""
	_cmd_name = "cmd_help"
	_result = None
	if update.effective_chat.type == "private":
		_result = "*msg__help"
		update.message.reply_text(__help["en"], parse_mode=ParseMode.MARKDOWN, quote=True)
	else:
		_result = "*error__private_command_in_public"
		update.message.reply_text(
			"You can't ask this in public ! %s\nPlease [click here](https://telegram.me/%s?start=help)."
			% (emojize(":nerd_face:"), __bot_name),
			quote=True,
			parse_mode=ParseMode.MARKDOWN,
			disable_web_page_preview=True,
		)
	if _result is not None: Helper.log(_cmd_name, update, _result)


def event_group_join(bot, update):
	"""Reply when a member joins the group."""
	_greetings = True # Default behavior
	if str(update.effective_chat.id) in config["greetings"]:
		_greetings = config["greetings"][str(update.effective_chat.id)]
	if _greetings:
		if len(update.message.new_chat_members) == 1 and update.message.new_chat_member.is_bot:
			update.message.reply_text(
				"`0x4279652C20%s21`" % update.message.new_chat_member.username.encode("hex").upper(),
				parse_mode=ParseMode.MARKDOWN,
				quote=True
			)
		else:
			update.message.reply_text(
				"Hello, %s." % ', '.join([user.first_name for user in update.message.new_chat_members]),
				quote=True
			)


def event_group_leave(bot, update):
	"""Reply when a member leaves the group."""
	_greetings = True # Default behavior
	if str(update.effective_chat.id) in config["greetings"]:
		_greetings = config["greetings"][str(update.effective_chat.id)]
	if _greetings:
		if update.message.left_chat_member.is_bot:
			update.message.reply_text(
				"`0x4279652C20%s21`" % update.message.left_chat_member.username.encode("hex").upper(),
				parse_mode=ParseMode.MARKDOWN,
				quote=True
			)
		else:
			update.message.reply_text("Bye, %s." % update.message.left_chat_member.first_name, quote=True)


def save_config():
	Helper.save_file_json("config.json", config)


def cmd_greetings(bot, update, args):
	"""Disable greetings """
	_cmd_name = "cmd_greetings"
	_result = None
	if args[0].lower() == "on":
		_activate = True
	elif args[0].lower() == "off":
		_activate = False
	else:
		_activate = None
	_check_admins = False
	_do = False
	if update.effective_chat.type in ["group", "supergroup"] and _activate is not None:
		if str(update.effective_chat.id) in config["greetings"]:
			if config["greetings"][str(update.effective_chat.id)] is not _activate:
				_check_admins = True
		else:
			_check_admins = True
	if _check_admins:
		if update.effective_chat.all_members_are_administrators:
			_do = True
			print("dew it")
		else:
			_admins = update.effective_chat.get_administrators() # Type: telegram.ChatMember
			if update.effective_user.id in [admin.user.id for admin in _admins]:
				_do = True
				print("dew it")
	if _do:
		config["greetings"][str(update.effective_chat.id)] = _activate
		save_config()
		update.message.reply_text("%s done!" % emojize(":thumbsup:", use_aliases=True), parse_mode=ParseMode.MARKDOWN)
		_result = "*greetings %s > %s" % (str(not _activate), str(_activate))
	if _result is not None: Helper.log(_cmd_name, update, _result)


def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)


def cmd_start(bot, update, args):
	"""Send a message when the command /start is issued."""
	_cmd_name = "cmd_start"
	_result = None
	if update.effective_chat.type == "private":
		# Check if deep link
		if len(args) > 0:
			if args[0].lower() == "about":
				cmd_about(bot, update)
			elif args[0].lower() == "help":
				cmd_help(bot, update)
			else:
				_result = "*error__bad_deep_link"
				update.message.reply_text(
					'%s Bad deep link.\nUse /help to see how I can help you.'
					 % emojize(":thinking_face:", use_aliases=True)
				)
		else:
			_result = "*msg__start"
			update.message.reply_text('Hi !\nUse /help to see how I can help you.')
	if _result is not None: Helper.log(_cmd_name, update, _result)


def cmd_send_log(bot, update):
	"""
	Send logs to (admin) user
	"""
	_cmd_name = "cmd_send_log"
	_result = None
	# Check if admin
	if update.effective_chat.id in config["admins"]:
		_result = str(update.effective_user.id)
		with open("log.csv", "rb") as _file:
			_file_name = "%s-log-%s.csv" % (config["bot_name"], datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H-%M-%S"))
			bot.sendDocument(
				chat_id=update.effective_user.id,
				document=_file,
				reply_to_message_id=update.message.message_id,
				caption="Here you are!",
				filename=_file_name
			)
	if _result is not None: Helper.log(_cmd_name, update, _result)


def bot_set_handlers(dispatcher):
	"""Register handlers for the Telegram commands"""
	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("start", cmd_start, pass_args=True))
	dispatcher.add_handler(CommandHandler("help", cmd_help))
	dispatcher.add_handler(CommandHandler("about", cmd_about))
	dispatcher.add_handler(CommandHandler("convert", cmd_convert, pass_args=True))
	dispatcher.add_handler(CommandHandler("price", cmd_price, pass_args=True))
	#dispatcher.add_handler(CommandHandler("snap", cmd_snap, pass_args=True))
	dispatcher.add_handler(CommandHandler("ticker", cmd_ticker, pass_args=True))
	dispatcher.add_handler(CommandHandler("keskifichou", cmd_easter_egg))
	#dispatcher.add_handler(CommandHandler("greetings", cmd_greetings, pass_args=True))
	dispatcher.add_handler(CommandHandler("get_log", cmd_send_log, pass_args=False))
	dispatcher.add_handler(InlineQueryHandler(inline_query))

	# quand quelqu'un rejoint/quitte le chat
	#dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, event_group_join))
	#dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, event_group_leave))

	# log all errors
	dispatcher.add_error_handler(error)


def bot_init():
	# Create the EventHandler and pass it your bot's token.
	updater = Updater(config["token"][__dev])
	# Get the dispatcher to register handlers
	bot_set_handlers(updater.dispatcher)
	# Start the Bot
	if config["webhook"]["enable"]:
		updater.start_webhook(
			listen="0.0.0.0",
			port=config["webhook"]["port"],
			url_path=config["token"][__dev],
			key="server.key",
			cert="server.pem",
			webhook_url="%(url)s:%(port)s/" % (config["webhook"]) + config["token"][__dev]
		)
	else:
		updater.start_polling(clean=True)
	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


def main():
	"""Start the bot."""
	bot_init()
	# Generate a coin list from CoinMarketCap
	if not __debug: api_coinmarketcap.generate_cmc_coinlist()


if __name__ == '__main__':
	#try:
	#	assert not config["webhook"]["enable"]
	Helper.log_("main", "", "", "")
	main()
	#except AssertionError:
	#	print("Can't run the bot: Webhook is enabled.")
