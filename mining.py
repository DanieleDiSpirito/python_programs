from hashlib import sha256
from os import urandom as rand_bytes
from sys import argv

while True:
    PoW = rand_bytes(16)
    if sha256(PoW).digest().hex().startswith('00'*int(argv[1])):
        print(PoW, sha256(PoW).digest().hex(), sep = '\n')
        break
