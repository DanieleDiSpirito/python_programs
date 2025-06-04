from time import perf_counter
from collections import deque

# O(n^2)
def list_solution(array: list[int], jump: int ) -> list:
	res: list[int] = []
	index = 0
	while array: # O(n)
		index = (index+jump-1) % len(array)
		n = array.pop(index) # O(n)
		res.append(n)
	return res

# O(n*jump)
def opt_solution(array: list[int], jump: int) -> list:
	res: list[int] = []
	index = 0
	array = deque(array)
	while array: # O(n)
		array.rotate(-(jump-1)) # O(jump)
		n = array.popleft() # O(1)
		res.append(n)
	return res

from tqdm import tqdm

time1, time2 = 0, 0

for nCase in tqdm(range(50+1)):
	N_SOLDIER = 10_000
	jump = 3
	soldier = list(range(1, N_SOLDIER+1))

	start = perf_counter()
	perm = list_solution(soldier, jump)
	end = perf_counter()
	time1 += end - start

	start = perf_counter()
	perm = opt_solution(soldier, jump) # opt if jump < n_soldier
	end = perf_counter()
	time2 += end - start
	N_SOLDIER += 100

print(time1) # ~ 2.8499078000095324s
print(time2) # ~ 0.0022822000209998805s

