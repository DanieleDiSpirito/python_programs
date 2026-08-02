# LVN (Local Value Numbering)

'''
# | Value | Var
1 |     4 | a <- a
2 |     7 | b <- b
3 | #1+#2 | c <- c, e
4 | #3*#3 | d <- d, f

6 vars for 4 values
'''

from sys import argv
from read_json import read_json
from copy import deepcopy
import json
import os

assert len(argv) == 2, "Usage: python3 lvn.py <file.json>"

obj = read_json(argv[1])
instrs = obj['functions'][0]['instrs']

'''
{'dest': 'a', 'op': 'const', 'type': 'int', 'value': 3}
{'dest': 'b', 'op': 'const', 'type': 'int', 'value': 4}
{'dest': 'g', 'op': 'const', 'type': 'int', 'value': 3}
{'args': ['a', 'b'], 'dest': 'c', 'op': 'add', 'type': 'int'}
{'args': ['c'], 'dest': 'd', 'op': 'id', 'type': 'int'}
{'args': ['d'], 'dest': 'e', 'op': 'id', 'type': 'int'}
{'args': ['d', 'e'], 'dest': 'f', 'op': 'mul', 'type': 'int'}
'''

table = {}
var2num = {}

j = 1

for i in instrs:
	if 'dest' in i:
		if i['op'] == 'const':
			if i['value'] not in table:
				table[i['value']] = j
				j += 1
			var2num[i['dest']] = table[i['value']]
		elif i['op'] == 'id':
			var2num[i['dest']] = var2num[i['args'][0]]
		else:
			args = [var2num[x] for x in i['args']]
			tup = (i['op'], *args)
			if tup not in table:
				table[tup] = j
				j += 1
			var2num[i['dest']] = table[tup]

new_instrs = deepcopy(instrs)

for i in new_instrs:
	if 'args' in i:
		args = [f'v{var2num[x]:02}' for x in i['args']]
		i['args'] = args
	if 'dest' in i:
		i['dest'] = f"v{var2num[i['dest']]:02}"

used_num = set()
to_pop = []

for idx, i in enumerate(new_instrs):
	if 'dest' in i:
		if i['op'] == 'id' and i['dest'] == i['args'][0]:
			to_pop.append(idx)		
		elif i['dest'] in used_num: # REMINDER: CODE VALID ONLY FOR SSA
			to_pop.append(idx)
		else:
			used_num.add(i['dest'])

for k, idx in enumerate(to_pop):
	new_instrs.pop(idx - k)

obj['functions'][0]['instrs'] = new_instrs

new_filename = argv[1].replace('.json', '_opt-lvn.json')

with open(new_filename, 'w') as f:
   f.write(json.dumps(obj, indent=2))

bril_new_file = new_filename.replace('.json', '.bril')

os.popen(f"bril2txt < {new_filename} > {bril_new_file}")

print(f'\nNew program ({bril_new_file}):')
print(os.popen(f"cat {bril_new_file}").read())
