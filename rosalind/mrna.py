from prot import codon_table

rev_codon = {}
for seq, prot in codon_table.items():
	if prot not in rev_codon:
		rev_codon[prot] = []
	rev_codon[prot].append(seq)

MODULO = 1_000_000

if __name__ == '__main__':
	from sys import argv
	assert len(argv) == 2, "Command: py %s <string>" % argv[0]
	s = argv[1]

	l = [len(rev_codon[prot]) for prot in s]
	l.append(len(rev_codon['_'])) # stop seq

	res = 1
	for el in l:
		res *= el
		res %= MODULO

	print(f'{s}: {res}')
