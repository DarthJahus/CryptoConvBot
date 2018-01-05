# coding=utf-8
# cryptoConBot

import logging
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from convertor import Converter_Convert, api_convert_coin
from emoji import emojize
import helperfunctions
import api_beach


# Config
dev = "mohus" # ou jahus
config = helperfunctions.load_file_json("config.json")


# VARIABLES
__version__ = "0.18.1.1"
__DONATION_ETH = ""
__DONATION_ETC = ""
__DONATION_XVG = ""
__DONATION_XRP = ""


# CONSTANTS
__help = {
	"fr": "*AIDE - HELP*\n\nFaire une conversion :\n/convert quantité monnaie_1 monnaie_2\n`Ex : /convert 1 ETH USD`'"
}

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a dew command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def start(bot, update):
	"""Send a message when the command /start is issued."""
	update.message.reply_text('Hi!')
	api_beach.generate_CMC_coinlist()


def about(bot, update):
	"""Send a message when the command /start is issued."""
	update.message.reply_text(
		'*CryptoConBot v %s*\npar %s @Jahus, %s @mohus, %s @foudre.\n\nAppelez /help pour voir la liste des commandes.'
		% (__version__, emojize(':robot_face:'), emojize(':alien_monster:'), emojize(':alien:')),
		parse_mode="Markdown",
		quote=True
	)


def convert(bot, update, args):
	print args
	update.message.reply_text(Converter_Convert(args), parse_mode="Markdown", quote=True)


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
					title='Error - Erreur',
					input_message_content=InputTextMessageContent("Failed to convert. Sorry.\n%s" % exchanges_result["result"], parse_mode=ParseMode.MARKDOWN),
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
					input_message_content=InputTextMessageContent(exchanges_result['result']['CryptoCompare'],parse_mode=ParseMode.MARKDOWN),
					description=exchanges_result['result_inline']['CryptoCompare'],
					thumb_url="https://i.imgur.com/LAOOxhM.png",
					thumb_height=64, thumb_width=64
				)
			),
			(
				InlineQueryResultArticle(
					id="Cryptonator000",
					title='Cryptonator',
					input_message_content=InputTextMessageContent(exchanges_result['result']['CryptoCompare'],parse_mode=ParseMode.MARKDOWN),
					description=exchanges_result['result_inline']['Cryptonator'],
					thumb_url="https://i.imgur.com/SoeT9GX.png",
					thumb_height=64, thumb_width=64
				)
			)
		]
	update.inline_query.answer(results)


def coinSnap (bot, update, args):
	if (len(args) > 2):
		# trop d'argument
		update.message.reply_text("*ERROR - ERREUR*\n"
								  "*Utilisation :* `snap monnaie0 monnaie1`\n"
								  "_monnaie1 est optionel, le cas échéant, la conversion se fait vers l'USD_", parse_mode="Markdown")
	else:
			# si une seule monnaie a été spécifiée
		if len(args) == 1:
			# un seul argument a été passé (la monnaie qui nous intéresse)
			# alors la conversion se fera par défaut vers l'USD
			api_beach.api_coinmarketcap_getSnap(args[0], 'usd')
		else :
			# la conversion prend en considération deux monnaies
			api_beach.api_coinmarketcap_getSnap(args[0], args[1])

def help(bot, update):
	"""Send a message when the command /help is issued."""
	update.message.reply_text(__help["fr"], parse_mode="Markdown")


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
	dp.add_handler(CommandHandler("convert", convert, pass_args= True))
	dp.add_handler(InlineQueryHandler(inlinequery))
	dp.add_handler(CommandHandler("snap", coinSnap, pass_args=True))


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

