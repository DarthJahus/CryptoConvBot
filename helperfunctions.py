import json


def load_file_json(file_name):
	with open(file_name, 'r') as _file:
		content = _file.read()
		content_dict = json.loads(content)
		_file.close()
		return content_dict

def save_file_json(file_name, args):
	with open(file_name, 'w') as _file:
		json.dump(args, _file, ensure_ascii=False, encoding="utf-8")
		_file.close()
