from sys import stdout
import time
from threading import Thread
from random import randint
from tqdm import tqdm

def smart_print(string: str):
	stdout.write(string + ' ')
	stdout.flush()

def sleeping(num: int):
	global denom, idx
	time.sleep(num/denom)
	smart_print(str(num))
	#res[idx] = num
	#idx += 1

LEN = 100
success: int = 0 # 23% with num/1_000 | 100% with num/100 | 45% with num/500 | 65% with num/300 | 95% with num/200 | 99% with num/150
failed: bool = False
denom = 150
'''
for j in tqdm(range(100)):
	array = [randint(0, 100) for i in range(LEN)]
	threads = [0]*LEN
	res = [0]*LEN
	idx = 0
	for i, el in enumerate(array):
		t = Thread(target=sleeping, args=(el,))
		threads[i] = t
		t.start()
	for t in threads:
		t.join()
	if res == sorted(array): success += 1
	else: failed += 1

print(success, failed)
'''

array = [randint(0, 10_000) for i in range(LEN)]
threads = [0]*LEN
res = [0]*LEN
idx = 0
for i, el in enumerate(array):
		t = Thread(target=sleeping, args=(el,))
		threads[i] = t
		t.start()
for t in threads:
	t.join()
