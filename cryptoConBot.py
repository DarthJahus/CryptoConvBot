# coding=utf-8
# cryptoConBot

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from convertor import Converter_Convert

# VARIABLES

__version = "0.18.1.3"


# CONSTANTES

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
	update.message.reply_text(Converter_Convert(args), parse_mode="Markdown")

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('*AIDE - HELP*\n\nFaire une conversion :\n/convert quantité monnaie_1 monnaie_2\n\t\t`Ex : /convert 1 ETH USD`', parse_mode="Markdown")

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

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

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

