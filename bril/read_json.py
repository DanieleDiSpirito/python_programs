import json

def read_json(filename: str):
	with open(filename, 'r') as file:
		f = file.read()
	obj = json.loads(f)
	return obj
