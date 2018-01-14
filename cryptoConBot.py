# coding=utf-8
# cryptoConBot

import logging
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, utils, Chat
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, Filters, MessageHandler
from convertor import Converter_Convert, api_convert_coin
from emoji import emojize
import helperfunctions as Helper
import api_beach

# Config
dev = "mohus"  # ou jahus
config = Helper.load_file_json("config.json")

# VARIABLES
__version__ = "0.18.1.3"
__bot_name = "cryptoconvbot"
__DONATION_ETH = "0x624688e4012c9E6Be7239BeA0A575F8e41B4B3B6"
__DONATION_XVG = "DCY3HQXo8JtTGomK1673QgT4rkX8rdyZXA"
__DONATION_PND = "PEwzKUUf1noKQaSkzKinPZ6irJBL1WckB4"
__DONATION_BTC = "1EnQoCTGBgeQfDKqEWzyQLaKWQbP2YR1uU"


# CONSTANTS
__help = {
	"fr": "*HELP* %s\n\n*Conversion :*\n/convert amount coin1 coin2\n::` /convert 1 ETH USD`"
	      "\n\n*Get ticker :*\n/ticker coin\n::`  /ticker BCH`\n\n*Get snapshot of coin :*\n/snap coin\n::`  /snap ETH`"
			"\n\n*INLINE MODE* %s\n"
	      "This bot can bot used in inline mode to convert, just write :\n"
	      "`@CryptoConvBot`"
			% (emojize(":key:"), emojize(":arrow_right_hook:", use_aliases=True))
}

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.CRITICAL
)
logger = logging.getLogger(__name__)


# Define a dew command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def start(bot, update):
	"""Send a message when the command /start is issued."""
	update.message.reply_text('Hi !\nPlease type and send /help to see how it works...')
	api_beach.generate_cmc_coinlist()

def about(bot, update):
	"""Send a message when the command /start is issued."""

	if update.effective_chat.type == "private":
		update.message.reply_text(
			"*CryptoConBot v %s*\nby %s @Jahus, %s @mohus, %s @foudre.\n\nSend /help to see how it works :\n\n" \
			"*DONATIONS*\nIf you like our work, you can donate %s\n" \
			"*ETH/ETC:* `%s`\n" \
			"*XVG:* `%s`\n" \
			"*PND:* `%s`\n" \
			"*BTC/BCH:* `%s`\n" \
			"Thanks !\n\n*Credits* :\n"
			"API from [CryptoCoinMarket](https://coinmarketcap.com)\n" \
			"API from [Cryptonator](https://www.cryptonator.com)" \

			% (__version__, emojize(':robot_face:'), emojize(':alien_monster:'), emojize(':alien:'),
			   emojize(':beers:', use_aliases=True), __DONATION_ETH, __DONATION_XVG, __DONATION_PND, __DONATION_BTC),
			parse_mode=ParseMode.MARKDOWN,
			quote=True,
			disable_web_page_preview=True
		)
	else:
		update.message.reply_text("You can't ask this in public ! %s\nPlease [click here](https://telegram.me/%s?start=about)"
		                          % (emojize(":nerd_face:"), __bot_name),
		                          quote=True, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)

def convert(bot, update, args):
	update.message.reply_text(Converter_Convert(args), parse_mode=ParseMode.MARKDOWN, quote=True)

def ticker(bot, update, args):
	update.message.reply_text(Converter_Convert([args[0], "btc"]), parse_mode=ParseMode.MARKDOWN, quote=True)


def inlinequery(bot, update):
	query = update.inline_query.query

	if not query:
		return

	# on obtient les résultats de tous les exchanges (-query- contient la commande)
	# query est transformé en liste pour être décodé comme -args-
	exchanges_result = api_convert_coin(query.split(' '), inline_call=True)

	# elle contiendra la liste des "articles" inline à afficher
	results = list()

	if not exchanges_result["success"]:
		results = [
			(
				InlineQueryResultArticle(
					id="ErreurDeConversion000",
					title='Error (#32)',
					input_message_content=InputTextMessageContent(
						"Failed to convert. Sorry.\n%s" % exchanges_result["result"], parse_mode=ParseMode.MARKDOWN),
					description=("Failed to convert. Sorry.\n%s" % exchanges_result["result"]),
					thumb_url="http://i.imgur.com/vyxEwc9.png",
					thumb_height=64, thumb_width=64
				)
			)
		]
	else:
		results = [
			(
				InlineQueryResultArticle(
					id="CryptoCompare000",
					title='CryptoCompare',
					input_message_content=InputTextMessageContent(exchanges_result['result']['CryptoCompare'],
																  parse_mode=ParseMode.MARKDOWN),
					description=exchanges_result['result_inline']['CryptoCompare'],
					thumb_url="https://i.imgur.com/LAOOxhM.png",
					thumb_height=64, thumb_width=64
				)
			),
			(
				InlineQueryResultArticle(
					id="Cryptonator000",
					title='Cryptonator',
					input_message_content=InputTextMessageContent(exchanges_result['result']['CryptoCompare'],
																  parse_mode=ParseMode.MARKDOWN),
					description=exchanges_result['result_inline']['Cryptonator'],
					thumb_url="https://i.imgur.com/SoeT9GX.png",
					thumb_height=64, thumb_width=64
				)
			)
		]
	update.inline_query.answer(results)


def coinSnap(bot, update, args):
	if (len(args) > 2):
		# trop d'argument
		update.message.reply_text("*ERROR - ERREUR*\n"
								  "*Usage :* `snap coin0 coin1`\n"
								  "_coin1 is optional, in this case, conversion done in USD_",
								  parse_mode="Markdown")
	else:
		# si une seule monnaie a été spécifiée
		if len(args) == 1:
			# un seul argument a été passé (la monnaie qui nous intéresse)
			# alors la conversion se fera par défaut vers l'USD
			results = api_beach.api_coinmarketcap_getSnap(args[0], 'usd')
		else:
			# la conversion prend en considération deux monnaies
			results = api_beach.api_coinmarketcap_getSnap(args[0], args[1])

		if results["success"]==True:

			# on prend une emoji représentation un changement positif/négatif
			if results["result"]["change24"][0] == "-":
				_signEmo = emojize(":small_red_triangle_down:", use_aliases=True)
			else:
				_signEmo = emojize(":small_red_triangle:", use_aliases=True)

			# retour
			update.message.reply_text("*%s* (_%s_)\n\n*Price :* `%s USD - %s BTC`\n*Chang. 24h :* `%s` %s \n*Vol. 24h :* `%s USD`" %
											(args[0].upper(), results["result"]["coin_name"],  # la monnaie,
											results["result"]["price_usd"],
											results["result"]["price_btc"],
											results["result"]["change24"],  # valeur du changement sur 24h
											utils.helpers.escape_markdown(_signEmo),  # emoji affichange flèche haut/bas selon le changement
											results["result"]["24volume_usd"]),
										parse_mode=ParseMode.MARKDOWN)
		else:
			update.message.reply_text("*ERROR (#35)*", parse_mode=ParseMode.MARKDOWN)


def easterEgg(bot, update):
	update.message.reply_photo("https://i.imgur.com/gzjl0yD.jpg")

def help(bot, update):
	"""Send a message when the command /help is issued."""
	update.message.reply_text(__help["fr"], parse_mode=ParseMode.MARKDOWN,  quote=True)


# Un membre rejoint un groupe
def new_member(bot, update):
	msg = update.message
	# si le nouvel utilisateur est un bot, on ne dit rien
	# ***à débattre !!
	if not msg.new_chat_member.is_bot == True:
		update.message.reply_text("Hello, %s." % msg.new_chat_member.username, quote=True)

# Un membre quitte le groupe
def quit_member(bot, update):
	msg = update.message
	if not msg.new_chat_member.is_bot == True:
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
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("about", about))
	dp.add_handler(CommandHandler("convert", convert, pass_args=True))
	dp.add_handler(InlineQueryHandler(inlinequery))
	dp.add_handler(CommandHandler("snap", coinSnap, pass_args=True))
	dp.add_handler(CommandHandler("ticker", ticker, pass_args=True))
	dp.add_handler(CommandHandler("keskifichou", easterEgg))

	# quand quelqu'un rejoint/quitte le chat
	dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
	dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, quit_member))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
