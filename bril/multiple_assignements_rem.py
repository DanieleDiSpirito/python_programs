# Remove multiple assignements

'''
@main {
	a: int = const 1; <- erasable (no read before second assignement)
	b: int = const 2;
	a: int = const 3; <- second assignement
	d: int = add a b;
	print d;
}
'''

from sys import argv
from read_json import read_json
from copy import deepcopy
import json

assert len(argv) == 2, "Usage: python3 multiple_assigniments_rem.py <file.json>"

obj = read_json(argv[1])

instrs = obj['functions'][0]['instrs']

# [{'dest': 'a', 'op': 'const', 'type': 'int', 'value': 1}, {'dest': 'b', 'op': 'const', 'type': 'int', 'value': 2}, {'dest': 'c', 'op': 'const', 'type': 'int', 'value': 3}, {'args': ['a', 'b'], 'dest': 'd', 'op': 'add', 'type': 'int'}, {'args': ['d'], 'op': 'print'}]

assigned = {}
new_instrs = {}

to_rem = []

for i in instrs:
	if 'dest' in i:
		if assigned.get(i['dest']) is not None:
			to_rem.append(assigned.get(i['dest']))
		assigned[i['dest']] = (i, id(i))
	if 'args' in i:
		for arg in i['args']:
			print(f"removed {arg}, i: {i}")
			assigned.pop(arg, None)
	new_instrs[id(i)] = i

print()

print(to_rem)

for i, iid in to_rem:
	print(f"REMOVED {i}")
	new_instrs.pop(iid, None)

new_obj = deepcopy(obj)

new_obj['functions'][0]['instrs'] = list(new_instrs.values())

new_filename = argv[1].replace('.json', '_opt-ma.json')

with open(new_filename, 'w') as f:
	f.write(json.dumps(new_obj, indent=2))

