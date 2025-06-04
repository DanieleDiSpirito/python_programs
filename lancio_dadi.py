from sys import argv
import  matplotlib.pyplot as plt

n_times = int(argv[1])

res = {
	1: 1,
	2: 1,
	3: 1,
	4: 1,
	5: 1,
	6: 1,
}

for i in range(1, n_times):
	new_res = {}
	for n in range(1, 6+1):
		for j in range(i, 6*i + 1):
			if j+n in new_res: new_res[j+n] += res[j]
			else: new_res[j+n] = res[j]
	res = new_res

keys = res.keys()
values = res.values()

plt.bar(keys, values)
plt.show()