# coding=utf-8
# cryptoConBot

import logging
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from convertor import Converter_Convert, api_convert_coin

# VARIABLES

__version = "0.18.1.3"


# CONSTANTES

__help_FR = "*AIDE - HELP*\n\nFaire une conversion :\n/convert quantité monnaie_1 monnaie_2\n`Ex : /convert 1 ETH USD`'"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def start(bot, update):
	"""Send a message when the command /start is issued."""
	update.message.reply_text('Hi!')

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

	print exchanges_result

	results = list()

	results = [
		(InlineQueryResultArticle(
    	id="CryptoCompare000",
    	title='CryptoCompare',
		input_message_content=InputTextMessageContent(exchanges_result['result']['CryptoCompare'],parse_mode=ParseMode.MARKDOWN),
		description=exchanges_result['result']['CryptoCompare'],
		thumb_url="https://i.imgur.com/LAOOxhM.png",
		thumb_height=64, thumb_width=64)
	),
		(InlineQueryResultArticle(
    	id="Cryptonator000",
    	title='Cryptonator',
		input_message_content=InputTextMessageContent(exchanges_result['result']['CryptoCompare'],parse_mode=ParseMode.MARKDOWN),
		description=exchanges_result['result']['Cryptonator'],
		thumb_url="https://i.imgur.com/SoeT9GX.png",
		thumb_height=64, thumb_width=64)
		)]

	update.inline_query.answer(results)



def help(bot, update):
	"""Send a message when the command /help is issued."""
	update.message.reply_text(__help_FR, parse_mode="Markdown")

def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)


def main():
	"""Start the bot."""
	# Create the EventHandler and pass it your bot's token.
	updater = Updater("500043374:AAG7k0ksAhO-L6KXy8qBGXn3THda16t1Whg")

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("convert", convert, pass_args= True))
	dp.add_handler(InlineQueryHandler(inlinequery))


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

