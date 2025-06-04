from random import randint
from typing import Generator
from Crypto.Util.number import isPrime as is_prime # check with official library
from time import perf_counter

def gen_number(bit: int) -> int:
    return randint(2**(bit-1), 2**bit - 1) | 1

BIT = 4096

ATTEMPS = 25
success = 1 - 0.25**ATTEMPS
n_candidates = 0

def gen_primes(limit: int) -> Generator[int, None, None]:
    for i in range(2, limit):
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                break
        else:
            yield i

little_primes = list(gen_primes(10000))

isPrime = False
p = 1

start = perf_counter()
while not isPrime:
    p = gen_number(BIT)
    n_candidates += 1
    for x in little_primes:
        if p % x == 0:
            print(f"p is not prime: {p} % {x} == 0")
            break
    else:
        # check Miller-Rabin algorithm
        for i in range(ATTEMPS):
            isPrime = True
            a = randint(2, p - 1) | 1
            d = p - 1
            if pow(a, d, p) != 1:
                print(f"p is not prime: {a} ^ {d} % {p} != 1")
                isPrime = False
                break
            while d % 2 == 0:
                d //= 2
                if pow(a, d, p) == p - 1:
                    break
                if pow(a, d, p) != 1:
                    print(f"p is not prime: {a} ^ {d} % {p} != 1")
                    isPrime = False
                    break
end = perf_counter()

time_taken = end - start

if is_prime(p):
    print(f"p is prime: {p}\nfound in {n_candidates} candidates (in {time_taken:.2f} seconds)\nPrime probability: {success:.30%}")
else:
    raise ValueError(f"p is not prime: {p}")