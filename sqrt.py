from sys import argv
from decimal import Decimal, getcontext

N_ITER = 15
getcontext().prec = 15634 + 2

# ONLY FOR sqrt(4) = 2
# 15 iter -> 15634 decimal precision
# 14 iter -> 15634 // 2 decimal precision
# not a real precise pattern !!!

y = Decimal(int(argv[1]))
x = Decimal(y)

half = Decimal(0.5)

for i in range(N_ITER):
	x = Decimal(half * (x + y/x))
	print(f"sqrt({y}) = {x} after {i+1} iter")
