# number of results
n_results = 0

# max value of a, b and c
n = 100

#the variable 'start' help to optimize the execution
start = 0

result = []

stop = False

for a in range(n):
    for b in range(n):
        if a > b: start = a
        else: start = b
        for c in range(start, n):
            for x in range(len(result)):
                if c == result[x]: stop = True
            if stop:
                stop = False
                continue
            if a**2 + b**2 == c**2 and a != c and b != c:
                print(str(a) + ", " + str(b) + ", " + str(c))
                result.append(c)
                n_results += 1
                break #exist just a value of a and b where a^2 + b^2 = c^2

print("Number of results: " + str(n_results))
