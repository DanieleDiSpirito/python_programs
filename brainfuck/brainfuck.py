'''
> = increases memory pointer, or moves the pointer to the right 1 block.
< = decreases memory pointer, or moves the pointer to the left 1 block.
+ = increases value stored at the block pointed to by the memory pointer
- = decreases value stored at the block pointed to by the memory pointer
[ = like c while(cur_block_value != 0) loop.
] = if block currently pointed to's value is not zero, jump back to [
, = like c getchar(). input 1 character.
. = like c putchar(). print 1 character to the console
'''

from sys import argv

LEN = 30_000

S = [0] * LEN
i = [0]
j = [0]

def increasePointer():
	i[0] = (i[0] + 1) % LEN

def decreasePointer():
	i[0] = (i[0] - 1) % LEN

def increaseValue():
	S[i[0]] += 1

def decreaseValue():
	S[i[0]] -= 1

def startLoop():
	j[0] = k[0]
	if S[i[0]] == 0:
		while k[0] < len(program) and program[k[0]] != ']':
			k[0] += 1
		assert k[0] < len(program), 'While loop not closed'

def endLoop():
	k[0] = j[0] - 1

def inputValue():
	S[i[0]] = int(input())

def printValue():
	print(S[i[0]])


op = {
	'>': increasePointer,
	'<': decreasePointer,
	'+': increaseValue,
	'-': decreaseValue,
	'[': startLoop,
	']': endLoop,
	',': inputValue,
	'.': printValue
}

assert len(argv) >= 2, 'python3 brainfuck.py <input_file>'
with open(argv[1], 'r') as f:
	program = f.read()[:-1]

k = [0]
while k[0] < len(program):
	command = program[k[0]]
	op[command]()
	k[0] += 1
