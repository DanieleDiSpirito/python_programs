# FASTA to lines

def fasta2lines(s: str) -> list:
	lines = []
	last_line = ''
	for line in s.split('\n'):
		if not line.startswith('>'):
			last_line += line
		else:
			lines.append(last_line)
			last_line = ''
	lines = lines[1:]
	lines.append(last_line)
	return lines

