from random import random as rand
from matplotlib import pyplot as plt


STARTING_POINT = 100
LOOPS = 1000


if __name__ == '__main__':
    values = [0 for _ in range(LOOPS)]
    values[0] = STARTING_POINT
    for idx in range(1, LOOPS):
        new_value = (1 + (rand() - 0.5) / 10) * values[idx-1]
        values[idx] = new_value
    print("Starting point:", STARTING_POINT)
    print("Final value:", values[-1])
    print("Trend: {symbol}{trend:.2f}%".format(trend = 100 * (values[-1]  - STARTING_POINT) / STARTING_POINT, symbol = "+" if values[-1] > STARTING_POINT else ""))
    print("Average value:", sum(values) / len(values))
    print("Max value:", max(values))
    print("Min value:", min(values))
    print("Range:", max(values) - min(values))
    plt.plot(values)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Random Stock Trend')
    plt.show()
