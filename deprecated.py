#####--------------------------------------

def cmd_snap(update : Update, context : CallbackContext):
	_cmd_name = "cmd_snap"
	_result = None
	if len(context.args) > 1:
		# too many arguments
		_result = "*error__too_many_args"
		update.message.reply_text(
			"*Error :(*\n"
			"*Usage :* `/snap <coin0>`\n",
			parse_mode="Markdown"
		)
	else:
		# ETH by default, for @Seynon, USD is still retrieved
		_unit_source = context.args[0].lower()
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
					context.args[0].upper(), _results["result"]["coin_name"],
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


#####--------------------------------------

def cmd_easter_egg(update : Update):
	update.message.reply_photo("https://i.imgur.com/gzjl0yD.jpg")


#####--------------------------------------


# OLD-PRICE COMMAND (on Cryptonar API)
""" def cmd_price(update : Update, context : CallbackContext):
	_cmd_name = "cmd_price"
	if len(context.args) == 1:
		_result = "[%s]" % ', '.join(context.args).replace('\n', '\\n')
		_message = convert([context.args[0], "usd"]) + get_advertisement()
	elif len(context.args) == 0:
		_result = None
		_message = None
	else:
		_result = "*error__invalid_query [%s]" % ", ".join(context.args).replace("\n", "\\n")
		_message = "Error: Invalid query:\n%s" % context.args
	if _result is not None:
		context.bot.send_message(update.effective_chat.id, _message, parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id, disable_web_page_preview=True)
		Helper.log(_cmd_name, update, _result) """


def event_group_join(update: Update):
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


def event_group_leave(update: Update):
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


def cmd_greetings(update: Update, context: CallbackContext):
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
