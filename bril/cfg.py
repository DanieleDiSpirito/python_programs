from basic_block import retrieve_blocks
import json
from sys import argv
import graphviz

assert len(argv) == 2, "Usage: cgf.py <file.json>"

with open(argv[1], 'r') as file:
   f = file.read()
obj = json.loads(f)

instrs = obj['functions'][0]['instrs']

blocks = list(retrieve_blocks(instrs))

def retrieve_cfg(blocks):
	cfg = {}
	for idx, block in enumerate(blocks):
		instrs = block[1]
		name = block[0]
		if 'op' in instrs[-1] and instrs[-1]['op'] == 'jmp':
			cfg[name] = {instrs[-1]['labels'][0]}
		elif 'op' in instrs[-1] and instrs[-1]['op'] == 'br':
			cfg[name] = {*instrs[-1]['labels']}
		elif idx + 1 < len(blocks):
			cfg[name] = {blocks[idx+1][0]}
	return cfg

cfg = retrieve_cfg(blocks)

def format_instr(i):
	if 'label' in i:
		return f".{i['label']}:"
	if 'dest' in i:
		if i.get('op') == 'const':
			return f"{i['dest']}: {i['type']} = const {i['value']}"
		args = ' '.join(i.get('args', []))
		if 'type' in i:
			return f"{i['dest']}: {i['type']} = {i['op']} {args}"
		return f"{i['dest']} = {i['op']} {args}"
	args = ' '.join(i.get('args', []))
	labels = ' '.join(f".{l}" for l in i.get('labels', []))
	return f"{i['op']} {args} {labels}".strip()

if __name__ == '__main__':

	node_labels = {}
	for block in blocks:
		name = block[0]
		instrs = block[1]
		formatted_lines = [format_instr(i) for i in instrs]
		node_labels[name] = f".{name}\n" + "\n".join(formatted_lines)

	dot = graphviz.Digraph(comment='Control Flow Graph', format='png')
	dot.attr(rankdir='TB', nodesep='0.6', ranksep='0.6')

	dot.attr('node', 
         shape='box', 
         style='filled,rounded', 
         fillcolor='#f4f7f6', 
         color='#4a5568', 
         fontname='Courier New', 
         fontsize='10', 
         align='left')
	dot.attr('edge', 
         color='#718096', 
         arrowhead='vee', 
         arrowsize='0.8', 
         penwidth='1.2')

	for node_name, label_content in node_labels.items():
   	 dot.node(node_name, label=label_content)

	for node, neighbors in cfg.items():
   	 for neighbor in neighbors:
      	  dot.edge(node, neighbor)

	dot.render(argv[1].replace('.json', ''), view=True)

