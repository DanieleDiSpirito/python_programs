from random import randint as r

print('#' + ''.join([hex(r(0, 15))[2:] for _ in range(6)]))
