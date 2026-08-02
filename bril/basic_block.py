import json
from sys import argv

assert len(argv) == 2, "Usage: basic_block.py <file.json>"

with open(argv[1], 'r') as file:
	f = file.read()
obj = json.loads(f)

instrs = obj['functions'][0]['instrs']

TERMINATORS = ['jmp', 'br']

def retrieve_blocks(instrs):
	name = 'main'
	block = []
	for instr in instrs:
		if 'label' in instr:
			if len(block) > 0:
				yield (name, block)
				block = []
			name = instr['label']
		elif 'op' in instr and instr['op'] in TERMINATORS:
			block.append(instr)
			yield (name, block)
			name = ""
			block = []
		else:
			block.append(instr)
	if len(block) > 0:
		yield (name, block)


if __name__ == "__main__":
	
	blocks = list(retrieve_blocks(instrs))
	for block in blocks:
		print(f'.{block[0]}: {block[1]}')

# {'functions': [{'args': [{'name': 'n', 'type': 'int'}], 'instrs': [{'dest': 'x', 'op': 'n', 'type': 'int'}, {'dest': 'zero', 'op': 'const', 'type': 'int', 'value': 0}, {'dest': 'one', 'op': 'const', 'type': 'int', 'value': 1}, {'dest': 'result', 'op': 'one', 'type': 'int'}, {'label': 'cond'}, {'args': ['x', 'zero'], 'dest': 'b', 'op': 'gt', 'type': 'bool'}, {'args': ['b'], 'labels': ['iter', 'stop'], 'op': 'br'}, {'label': 'iter'}, {'args': ['result', 'x'], 'dest': 'result', 'op': 'mul'}, {'args': ['x', 'one'], 'dest': 'x', 'op': 'sub'}, {'labels': ['cond'], 'op': 'jmp'}, {'label': 'stop'}, {'args': ['result'], 'op': 'print'}], 'name': 'main'}]}
