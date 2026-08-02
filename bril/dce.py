# DCE (Dead Code Elimination)

'''
@main {
	a: int = const 1;
	b: int = const 2;
	c: int = const 3; <- erasable (never used)
	d: int = add a b;
	print d;
}
'''

from sys import argv
from read_json import read_json
from copy import deepcopy
import json
import os

assert len(argv) == 2, "Usage: python3 dce.py <file.json>"

obj = read_json(argv[1])

instrs = obj['functions'][0]['instrs']

# [{'dest': 'a', 'op': 'const', 'type': 'int', 'value': 1}, {'dest': 'b', 'op': 'const', 'type': 'int', 'value': 2}, {'dest': 'c', 'op': 'const', 'type': 'int', 'value': 3}, {'args': ['a', 'b'], 'dest': 'd', 'op': 'add', 'type': 'int'}, {'args': ['d'], 'op': 'print'}]

while True:
	used = {}
	new_instrs = {}

	for i in instrs:
		if 'dest' in i:
			used[i['dest']] = (i, id(i))
			print(f"added {i['dest']}, i: {i}")
		if 'args' in i:
			for arg in i['args']:
				print(f"removed {arg}, i: {i}")
				used.pop(arg, None)
		new_instrs[id(i)] = i

	print()

	for var, i in used.items():
		print(f"REMOVED {i[0]}")
		new_instrs.pop(i[1], None)

	print(instrs)
	instrs = list(new_instrs.values())	
	print(instrs)
	
	if len(used) == 0: break

new_obj = deepcopy(obj)

new_obj['functions'][0]['instrs'] = list(new_instrs.values())

new_filename = argv[1].replace('.json', '_opt-dce.json')

with open(new_filename, 'w') as f:
	f.write(json.dumps(new_obj, indent=2))

bril_new_file = new_filename.replace('.json', '.bril')

os.popen(f"bril2txt < {new_filename} > {bril_new_file}")

print(f'\nNew program ({bril_new_file}):')
print(os.popen(f"cat {bril_new_file}").read())
