# Forward Data Flow

from sys import argv
from read_json import read_json
from basic_block import retrieve_blocks
from cfg import retrieve_cfg
from collections import deque

assert len(argv) == 2, "Usage: python3 formard_data_flow.py <file.json>"

obj = read_json(argv[1])

instrs = obj['functions'][0]['instrs']

blocks = list(retrieve_blocks(instrs))
cfg = retrieve_cfg(blocks)

for b in blocks:
	if b[0] not in cfg:
		cfg[b[0]] = set()

blocks_dict = {b[0]: b[1] for b in blocks}

def merge(sets):
	result = set()
	for s in sets:
		result |= s
	return result

def transfer(b, in_b):
	gen = set()
	kill = set()
	defined_here = set()
	for i in blocks_dict[b]:
		if 'dest' in i:
			var = i['dest']
			defined_here.add(var)
	kill = {(v, d) for (v, d) in in_b if v in defined_here}
	gen = {(var, b) for var in defined_here}
	return gen | (in_b - kill)

init = set()

IN = {}
OUT = {}

IN[blocks[0][0]] = init
for b in blocks:
	OUT[b[0]] = init

worklist = deque(b[0] for b in blocks)

revcfg = {b[0]: set() for b in blocks}

for k, v in cfg.items():
	for value in v:
		revcfg[value].add(k)

while worklist:
	b = worklist.popleft()
	preds = revcfg[b]
	if preds:
		IN[b] = merge([OUT[p] for p in preds])
	else:
		IN[b] = init
		
	prev = OUT[b]
	OUT[b] = transfer(b, IN[b])
	if prev != OUT[b]:
		worklist.extend(cfg[b])

print(f'{IN=}')
print(f'{OUT=}')
