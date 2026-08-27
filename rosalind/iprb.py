from sys import argv

if __name__ == '__main__':
	assert len(argv) == 4, "Bad args"
	count = [int(argv[i]) for i in range(1, 4)]

def P(class1: int, class2: int) -> float:
	n = sum(count)
	c1 = count[class1]
	c2 = count[class2]
	if class1 == class2:
		c2 -= 1
		c2 /= 2
	return (2 * c1 * c2) / (n * (n-1))

if __name__ == '__main__':
	res = P(0,0) + P(0,1) + P(0,2) + 0.75 * P(1,1) + 0.5 * P(1,2)
	print(res)
