#!/usr/bin/python3
# coding=utf-8

import logging
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackContext
from telegram.update import Update
from emoji import emojize
import urllib3
urllib3.disable_warnings()
from datetime import datetime
import time
from random import choices

# modularity [internal bot modules]
import constants as consts
from Converter import convert, api_convert_coin
import helperfunctions as Helper

import api_nomics
import api_coinmarketcap

# Config
__dev = "mohus_test"  # "test" for tests, "bot" for production
__debug = False
config = Helper.load_file_json("config.json")

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.ERROR #CRITICAL
)
logger = logging.getLogger(__name__)


def get_advertisement():
	_messages = []
	_rates = []
	for _item in consts.__advertisements:
		if  consts.__advertisements[_item]["message"] is None:
			_messages.append("")
		else:
			_messages.append("\n\n%s [%s](%s)" % (emojize( consts.__advertisements[_item]["emoji"], use_aliases=True),  consts.__advertisements[_item]["message"],  consts.__advertisements[_item]["url"]))
		_rates.append( consts.__advertisements[_item]["rate"])
	return choices(_messages, _rates)[0]


def cmd_about(update : Update, context : CallbackContext):
	"""Send a message when the command /start is issued."""
	_cmd_name = "cmd_about"
	_result = None
	if update.effective_chat.type == "private":
		_result = "*msg__about"
		context.bot.send_message(
			update.effective_chat.id, 
			consts.__ABOUT_TEXT,  
			parse_mode=ParseMode.MARKDOWN, 
			reply_to_message_id=update.message.message_id, 
			disable_web_page_preview=True)
	else:
		_result = "error__private_command_in_public"
		context.bot.send_message(
			update.effective_chat.id, 
			"You can't ask this in public ! %s\nPlease [click here](https://telegram.me/%s?start=about)." % (emojize(":nerd_face:"),  consts.__bot_name),  
			parse_mode=ParseMode.MARKDOWN, 
			reply_to_message_id=update.message.message_id, 
			disable_web_page_preview=True)

	if _result is not None: Helper.log(_cmd_name, update, _result)


def cmd_convert(update : Update, context : CallbackContext):
	_cmd_name = "cmd_convert"
	if len(context.args) in [2, 3]:
		_result = "[%s]" % ', '.join(context.args).replace('\n', '\\n')
		_message = convert(context.args) + get_advertisement()
	elif len(context.args) == 0:
		_result = None
		_message = None
	else:
		_result = "*error__invalid_query [%s]" % ", ".join(context.args).replace("\n", "\\n")
		_message = "Invalid query.\n[See help](https://t.me/cryptoconvbot?start=help)"
	if _result is not None:
		context.bot.send_message(update.effective_chat.id, _message, parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)
		Helper.log(_cmd_name, update, _result)


def cmd_ticker(update : Update, context : CallbackContext):
	_cmd_name = "cmd_ticker"
	if len(context.args) == 1:
		_result = "[%s]" % ', '.join(context.args).replace('\n', '\\n')
		_message = convert([context.args[0], "btc"]) + "\n\n **Try the new /price command !**" + get_advertisement()
	elif len(context.args) == 0:
		_result = None
		_message = None
	else:
		_result = "*error__invalid_query [%s]" % ", ".join(context.args).replace("\n", "\\n")
		_message = "Error: Invalid query:\n%s" % context.args
	if _result is not None:
		context.bot.send_message(update.effective_chat.id, _message, parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)
		Helper.log(_cmd_name, update, _result)



def inline_query(update : Update, context : CallbackContext):
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
				thumb_url= consts.__thumb_url["error"]["url"],
				thumb_height= consts.__thumb_url["error"]["height"],
				thumb_width= consts.__thumb_url["error"]["width"]
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
					thumb_url= consts.__thumb_url[service]["url"],
					thumb_width= consts.__thumb_url[service]["width"],
					thumb_height= consts.__thumb_url[service]["height"]
				)
			)
			_res_id+=1
		_result = "[%s]" % ', '.join(query.split()).replace('\n', '\\n')
	update.inline_query.answer(results)
	if _result is not None: Helper.log_(_cmd_name, update.effective_user.id, "{inline}", _result)


def cmd_price(update : Update, context : CallbackContext):
	_coin = context.args[0]
	_message = api_nomics.get_coin_price(_coin) + get_advertisement()

	context.bot.send_message(	update.effective_chat.id, 
								_message, parse_mode=ParseMode.MARKDOWN, 
								reply_to_message_id=update.message.message_id, 
								disable_web_page_preview=True)


def cmd_help(update : Update, context : CallbackContext):
	"""Send a message when the command /help is issued."""
	_cmd_name = "cmd_help"
	_result = None
	if update.effective_chat.type == "private":
		_result = "*msg__help"
		update.message.reply_text(consts.__help["en"], parse_mode=ParseMode.MARKDOWN, quote=True)
	else:
		_result = "*error__private_command_in_public"
		update.message.reply_text(
			"You can't ask this in public ! %s\nPlease [click here](https://telegram.me/%s?start=help)."
			% (emojize(":nerd_face:"),  consts.__bot_name),
			quote=True,
			parse_mode=ParseMode.MARKDOWN,
			disable_web_page_preview=True,
		)
	if _result is not None: Helper.log(_cmd_name, update, _result)


def event_group_join(update : Update):
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


def event_group_leave(update : Update):
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


def cmd_greetings(update : Update, context : CallbackContext):
	"""Disable greetings """
	_cmd_name = "cmd_greetings"
	_result = None
	if context.args[0].lower() == "on":
		_activate = True
	elif context.args[0].lower() == "off":
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



def cmd_start(update : Update, context : CallbackContext):
	"""Send a message when the command /start is issued."""
	_cmd_name = "cmd_start"
	_result = None
	if update.effective_chat.type == "private":
		# Check if deep link
		if len(context.args) > 0:
			if context.args[0].lower() == "about":
				cmd_about(context.bot, update)
			elif context.args[0].lower() == "help":
				cmd_help(context.bot, update)
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


def cmd_send_log(update : Update, context : CallbackContext):
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
			context.bot.sendDocument(
				chat_id=update.effective_user.id,
				document=_file,
				reply_to_message_id=update.message.message_id,
				caption="Here you are!",
				filename=_file_name
			)
	if _result is not None: Helper.log(_cmd_name, update, _result)


def error(update : Update, context : CallbackContext):
	"""Log Errors caused by Updates."""
	logger.error('Update "%s" caused error "%s"', update, context.error)


def bot_set_handlers(dispatcher):
	"""Register handlers for the Telegram commands"""
	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("start", cmd_start))
	dispatcher.add_handler(CommandHandler("help", cmd_help))
	dispatcher.add_handler(CommandHandler("about", cmd_about))
	dispatcher.add_handler(CommandHandler("convert", cmd_convert))
	dispatcher.add_handler(CommandHandler("price", cmd_price))
	dispatcher.add_handler(CommandHandler("ticker", cmd_ticker))
	dispatcher.add_handler(CommandHandler("get_log", cmd_send_log))
	dispatcher.add_handler(InlineQueryHandler(inline_query))


	#dispatcher.add_handler(CommandHandler("keskifichou", cmd_easter_egg))
	#dispatcher.add_handler(CommandHandler("greetings", cmd_greetings, pass_args=True))
		#dispatcher.add_handler(CommandHandler("price", cmd_price))		
	#dispatcher.add_handler(CommandHandler("snap", cmd_snap)) BYEEEEEEE


	# quand quelqu'un rejoint/quitte le chat
	#dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, event_group_join))
	#dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, event_group_leave))

	# log all errors
	dispatcher.add_error_handler(error)


def bot_init():
	# Create the EventHandler and pass it your bot's token.
	updater = Updater(config["token"][__dev], use_context=True)
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
	#if not __debug: api_coinmarketcap.generate_cmc_coinlist()


if __name__ == '__main__':
	#try:
	#	assert not config["webhook"]["enable"]
	Helper.log_("main", "", "", "")
	main()
	#except AssertionError:
	#	print("Can't run the bot: Webhook is enabled.")
