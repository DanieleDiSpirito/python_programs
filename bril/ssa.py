from read_json import read_json 
from basic_block import retrieve_blocks
from cfg import retrieve_cfg
from sys import argv

assert len(argv) == 2, "Usage: python3 ssa.py <file.json>"

obj = read_json(argv[1])

instrs = obj['functions'][0]['instrs']

blocks = list(retrieve_blocks(instrs))
cfg = retrieve_cfg(blocks)

# [{'label': 'entry'}, {'dest': 'a', 'op': 'const', 'type': 'int', 'value': 47}, {'dest': 'zero', 'op': 'const', 'type': 'int', 'value': 0}, {'args': ['a', 'zero'], 'dest': 'cond', 'op': 'gt', 'type': 'bool'}, {'args': ['cond'], 'labels': ['left', 'right'], 'op': 'br'}, {'label': 'left'}, {'args': ['a', 'a'], 'dest': 'a', 'op': 'add', 'type': 'int'}, {'labels': ['exit'], 'op': 'jmp'}, {'label': 'right'}, {'args': ['a', 'a'], 'dest': 'a', 'op': 'mul', 'type': 'int'}, {'labels': ['exit'], 'op': 'jmp'}, {'label': 'exit'}, {'args': ['a'], 'op': 'print'}]

revcfg = {} # get predecessors

for k, v in cfg.items():
	for value in v:
		if value not in revcfg:
			revcfg[value] = set()
		revcfg[value].add(k)

variables = set()

for i in instrs:
	if 'dest' in i:
		variables.add(i['dest'])

var = {block[0]: {v: None for v in variables} for block in blocks}
cnt = {block[0]: {v: 0 for v in variables} for block in blocks}

for block in blocks:
	print(f'.{block[0]}')
	ii = block[1]
	for i in ii:
		if 'dest' in i:
			v = i['dest']
			if var[block[0]][v] is None:
				new_v = f'{block[0]}.{v}'
				var[block[0]][v] = new_v
				cnt[block[0]][v] += 1
				print(f'{v} -> {new_v}')
				if block[0] in revcfg:
					for p in revcfg[block[0]]:
						new_command = ['phi']
						new_command.append(f".{p} {var[p][v]}")
						print(' '.join(new_command))
			else:
				cnt[block[0]][v] += 1
				c = cnt[block[0]][v]
				var[block[0]][v] = f'{block[0]}.{v}{c}'
				print(f'{v} -> {var[block[0]][v]}')