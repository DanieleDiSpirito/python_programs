def countAndSay(n: int) -> list[str]:
        def RLE(s: str) -> str:
            res = ''
            last = s[0]
            counter = 1
            for i in range(1, len(s)):
                if s[i] == last:
                    counter += 1
                else:
                    res += str(counter) + last
                    counter = 1
                    last = s[i]
            res += str(counter) + last
            return res

        countAndSay = [''] * n
        countAndSay[0] = '1'
        for i in range(1, n):
            countAndSay[i] = RLE(countAndSay[i-1])
        return [len(x) for x in countAndSay]

import matplotlib.pyplot as mpt
from math import exp

data = countAndSay(50)

# show data in histogram
mpt.bar(range(len(data)), data, color='black', alpha=0.5)
mpt.title('Count and Say')
mpt.xlabel('n')
mpt.ylabel('Length of Count and Say')
mpt.xticks(range(len(data)), range(1, len(data) + 1))
mpt.grid()
mpt.show()
