import json, time, codecs
from datetime import datetime


__debug = False


def load_file_json(file_name):
	with open(file_name, 'r') as _file:
		content = _file.read()
		content_dict = json.loads(content)
		_file.close()
		return content_dict


def save_file_json(file_name, args):
	with open(file_name, 'w', encoding="utf-8") as _file:
		json.dump(args, _file, ensure_ascii=False)
		_file.close()


def log_(command, user_id, chat_id, result):
	"""
	Log in a CSV file
	Header is:
	"time", "command", "user_id", "chat_id", "result"
	Time is in local-time
	"""
	_log = (
		datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H:%M:%S") + ',' +
		','.join([command, str(user_id), str(chat_id), "\"" + result + "\""]) + "\n"
	)
	with codecs.open("log.csv", 'a', "utf-8") as _file:
		_file.write(_log)
		if __debug: print("*log = " + _log)


def log(command, update, result):
	log_(
		command,
		"%s|@%s|%s|%s|%s" % (update.effective_user.id, update.effective_user.username, update.effective_user.first_name, update.effective_user.last_name, update.effective_user.language_code),
		"%s|@%s|%s|%s" % (update.effective_chat.id, update.effective_chat.username, update.effective_chat.title, update.effective_chat.type),
		result.replace("\n","\\n")
	)
