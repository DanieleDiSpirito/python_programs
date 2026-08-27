codon_table = {
	"UUU": "F",      "CUU": "L",      "AUU": "I",      "GUU": "V",
	"UUC": "F",      "CUC": "L",      "AUC": "I",      "GUC": "V",
	"UUA": "L",      "CUA": "L",      "AUA": "I",      "GUA": "V",
	"UUG": "L",      "CUG": "L",      "AUG": "M",      "GUG": "V",
	"UCU": "S",      "CCU": "P",      "ACU": "T",      "GCU": "A",
	"UCC": "S",      "CCC": "P",      "ACC": "T",      "GCC": "A",
	"UCA": "S",      "CCA": "P",      "ACA": "T",      "GCA": "A",
	"UCG": "S",      "CCG": "P",      "ACG": "T",      "GCG": "A",
	"UAU": "Y",      "CAU": "H",      "AAU": "N",      "GAU": "D",
	"UAC": "Y",      "CAC": "H",      "AAC": "N",      "GAC": "D",
	"UAA": "_",      "CAA": "Q",      "AAA": "K",      "GAA": "E",
	"UAG": "_",      "CAG": "Q",      "AAG": "K",      "GAG": "E",
	"UGU": "C",      "CGU": "R",      "AGU": "S",      "GGU": "G",
	"UGC": "C",      "CGC": "R",      "AGC": "S",      "GGC": "G",
	"UGA": "_",      "CGA": "R",      "AGA": "R",      "GGA": "G",
	"UGG": "W",      "CGG": "R",      "AGG": "R",      "GGG": "G",
}


from sys import argv

if __name__ == '__main__':
	assert len(argv) == 2, "Bad args"
	s = argv[1]
	res = ''.join([codon_table[s[i:i+3]] for i in range(0, len(s), 3)])
	assert res[-1] == '_', "Bad string"
	res = res[:-1]
	print(res)
