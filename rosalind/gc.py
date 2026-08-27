from sys import argv

assert len(argv) == 2, f"Usage: python3 {argv[0]} <filename.txt>"

try:
	with open(argv[1], 'r') as f:
		s = f.read().strip()
except FileNotFoundError as e:
	assert 0 == 1, "Bad file name"

def cg_content(ss: str) -> float:
	if len(ss) == 0:
		return 0.0
	return (ss.count('C') + ss.count('G')) / len(ss)
	
lines = s.split('\n')
lines.append('>end')

best_name = ""
best_score = 0.0
name = ""
ss = ""

for line in lines:
	if line.startswith('>'):
		score = cg_content(ss)
		if score > best_score:
			best_name = name
			best_score = score
		name = line.split('>')[1].strip()
		ss = ""
	else:
		ss += line

print(f'{best_name}\n{best_score*100:.6f}')

