from Crypto.Util.number import isPrime
import time

i = 1 # 0 is included
tot = 1
totPrime = 0

while True:
    tot += 1
    totPrime += isPrime(i)
    if isPrime(i):
        print(f'n: {i}, totPrime: {totPrime}, occ: {round(totPrime/i * 100, 3)}%')
    i += 1
    
